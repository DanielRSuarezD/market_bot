def check_alert(asset, change):

    if abs(change) >= 2:

        message = f"""
🚨 ALERTA DE MERCADO

{asset}: {change}%
"""

        return message

    return None