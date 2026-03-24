from plugins.base_plugin.base_plugin import BasePlugin
from utils.http_client import get_http_session
from datetime import date
import logging

logger = logging.getLogger(__name__)


class Wallos(BasePlugin):

    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['style_settings'] = True
        return template_params

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        host = settings.get("host", "").rstrip("/")
        api_key = settings.get("api_key", "")

        if not host:
            raise RuntimeError("Wallos URL ist nicht konfiguriert.")
        if not api_key:
            raise RuntimeError("Wallos API-Key ist nicht konfiguriert.")

        max_items = int(settings.get("max_items", 5))
        show_monthly_cost = settings.get("show_monthly_cost", "true") == "true"
        show_logos = settings.get("show_logos", "true") == "true"
        color_due_soon = settings.get("color_due_soon", "#c62828")
        color_due_week = settings.get("color_due_week", "#e65100")

        subscriptions, error = self._fetch_subscriptions(host, api_key, max_items)
        if subscriptions is None:
            raise RuntimeError(f"Konnte keine Verbindung zu Wallos herstellen: {error}")

        monthly_cost = None
        currency_symbol = ""
        if show_monthly_cost:
            monthly_cost, currency_symbol, error = self._fetch_monthly_cost(host, api_key)
            if monthly_cost is None:
                logger.warning("Monatskosten konnten nicht abgerufen werden: %s", error)

        template_params = {
            "subscriptions": subscriptions,
            "monthly_cost": monthly_cost,
            "currency_symbol": currency_symbol,
            "show_monthly_cost": show_monthly_cost,
            "show_logos": show_logos,
            "color_due_soon": color_due_soon,
            "color_due_week": color_due_week,
        }

        return self.render_image(dimensions, "wallos.html", "wallos.css", template_params)

    def _fetch_subscriptions(self, host, api_key, max_items):
        session = get_http_session()
        try:
            url = f"{host}/api/subscriptions/get_subscriptions.php?apiKey={api_key}&sort=next_payment&state=0"
            resp = session.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error("Wallos Abonnements konnten nicht abgerufen werden: %s", e)
            return None, str(e)

        raw_subs = data if isinstance(data, list) else data.get("subscriptions", [])

        today = date.today()
        subscriptions = []
        for sub in raw_subs:
            if sub.get("inactive") == 1:
                continue
            billing_date_str = sub.get("next_payment", "")
            try:
                billing_date = date.fromisoformat(billing_date_str)
                days_until = (billing_date - today).days
            except (ValueError, TypeError):
                billing_date = None
                days_until = None

            logo = sub.get("logo", "")
            logo_url = f"{host}/images/uploads/logos/{logo}" if logo else ""

            subscriptions.append({
                "name": sub.get("name", ""),
                "price": sub.get("price", 0),
                "next_payment": billing_date_str,
                "days_until": days_until,
                "logo_url": logo_url,
            })

        subscriptions.sort(key=lambda s: s["days_until"] if s["days_until"] is not None else 9999)
        return subscriptions[:max_items], None

    def _fetch_monthly_cost(self, host, api_key):
        session = get_http_session()
        today = date.today()
        try:
            url = f"{host}/api/subscriptions/get_monthly_cost.php?apiKey={api_key}&month={today.month}&year={today.year}"
            resp = session.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error("Wallos Monatskosten konnten nicht abgerufen werden: %s", e)
            return None, "", str(e)

        cost = data.get("localized_monthly_cost", data.get("monthly_cost", 0))
        symbol = data.get("currency_symbol", "")
        return cost, symbol, None
