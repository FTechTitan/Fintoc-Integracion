# Guía de Testing — Fintoc Demo

## URL del demo

https://payments-demo.techforce.cl

## Credenciales de prueba (Chile)

En el widget de Fintoc, seleccionar cualquier banco y usar:

| Campo | Valor |
|---|---|
| RUT | `41614850-3` |
| Password | `jonsnow` |
| Cuenta | `422159212` |

Esperar ~5 segundos → pago exitoso.

## Flujo completo

1. Ir a https://payments-demo.techforce.cl
2. Ingresar monto, email, ID reserva y nombre del alojamiento
3. Hacer clic en **Pagar con Fintoc**
4. El split se calcula automáticamente (20% TrypoPMS / 80% alojamiento)
5. Se abre el widget de Fintoc → seleccionar banco → usar creds de prueba
6. Confirmar cuenta `422159212` → pago procesado

## Simular MFA / autorización de contacto nuevo

Crear el checkout con un monto que termine en `01` (ej: `15001` CLP).
El widget pedirá autorizar el destinatario con dispositivo de seguridad.

## Trigger manual de evento (sin pasar por el widget)

```bash
source ~/.nvm/nvm.sh && nvm use 22 --silent
fintoc trigger payment_intent.succeeded
```

Simula un `payment_intent.succeeded` de $15.000 CLP directamente al webhook.

## Escuchar webhook en tiempo real (local)

```bash
source ~/.nvm/nvm.sh && nvm use 22 --silent
fintoc webhooks listen --forward-to http://localhost:5000/webhook
```

## Levantar el server localmente

```bash
set -a && source .env && set +a
BASE_URL=https://payments-demo.techforce.cl python3 demo/app.py
```

## Notas técnicas

- La API de Fintoc usa **Bearer token** (no Basic Auth como dice el README del CLI)
- `success_url` y `cancel_url` deben ser **HTTPS** — no acepta `http://localhost`
- El split en test mode se calcula pero el transfer real falla por balance $0
- Webhook secret: `whsec_test_sDQqWhPbd4StPXgeQ33qwnEv` (endpoint `we_l0vpOAqCe7jO8jEK`)
