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

## Testear el split completo (transfer real en test mode)

En test mode el balance arranca en $0, lo que bloquea el transfer al alojamiento.
Solución: simular un ingreso primero con el endpoint de Fintoc:

```bash
# 1. Simular ingreso de plata a la cuenta TrypoPMS
curl -s -X POST https://api.fintoc.com/v2/simulate/receive_transfer \
  -H "Authorization: Bearer $FINTOC_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number_id": "acno_3E8duaZmElIyXjJW1MnDkuoEdhY",
    "amount": 100000,
    "currency": "CLP",
    "counterparty_holder_name": "Cliente Demo"
  }'

# 2. Verificar balance
fintoc v2 accounts list

# 3. Ejecutar transfer de split al alojamiento
fintoc v2 transfers create \
  --amount 40000 \
  --currency CLP \
  --account-id acc_3E8duZcU6ELPNeOUjoeaCOolKbj \
  --counterparty-account-number 422159212 \
  --counterparty-institution-id cl_banco_estado \
  --counterparty-holder-id 41.614.850-3 \
  --counterparty-account-type checking_account \
  --comment "Split reserva DEMO-001 - alojamiento" \
  --jws-private-key /home/ftt/github/Fintoc-Integracion/jws_private_key.pem
```

### Resultado del test completo (2026-05-23)

| Paso | Detalle |
|---|---|
| Ingreso simulado | +$100.000 CLP → `tr_3E8uBEiJQJxVqymyIyLHODngu6c` |
| Pago de reserva | $50.000 CLP (PI `pi_3E8n2b3dtJsIVsiHf6ERM5WzCPi`, status: succeeded) |
| Transfer al alojamiento (80%) | -$40.000 → `tr_3E8uDVcGJphn0wc0oIzTen4tCKz`, status: pending |
| Balance TrypoPMS final | $60.000 CLP |

El transfer queda en `pending` en test mode — se procesa al día siguiente. En producción es casi inmediato.

## Pendiente para producción

Agregar en `demo/app.py` dentro del handler `payment_intent.succeeded` la llamada al transfer real:

```python
# En webhook(), dentro del if event["type"] == "payment_intent.succeeded":
fintoc_post("/v2/transfers", {
    "amount": split["alojamiento"],
    "currency": pi["currency"],
    "account_id": "acc_...",                        # cuenta TrypoPMS
    "counterparty_account_number": "...",            # cuenta del alojamiento
    "counterparty_institution_id": "cl_...",
    "counterparty_holder_id": "...",                 # RUT del alojamiento
    "counterparty_account_type": "checking_account",
    "comment": f"Split reserva {reserva}",
})
```

Requiere: JWS key configurada en Fintoc dashboard + balance > 0 (entra automático con pagos reales).

## Notas técnicas aprendidas

- La API de Fintoc usa **Bearer token** (no Basic Auth como dice el README del CLI)
- `success_url` y `cancel_url` deben ser **HTTPS** — no acepta `http://localhost`
- `v2 transfers create` requiere JWS key registrada en el dashboard
- El split se puede testear end-to-end en test mode usando `simulate/receive_transfer` primero
- Webhook secret: `whsec_test_sDQqWhPbd4StPXgeQ33qwnEv` (endpoint `we_l0vpOAqCe7jO8jEK`)
- Cuenta TrypoPMS: `acc_3E8duZcU6ELPNeOUjoeaCOolKbj` | Account number: `acno_3E8duaZmElIyXjJW1MnDkuoEdhY`
