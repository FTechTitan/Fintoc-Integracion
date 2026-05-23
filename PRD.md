# PRD — Demo Pagos + Split con Fintoc

## Objetivo

Validar los endpoints de Fintoc e implementar un demo funcional de:
1. Cobro al cliente via checkout session
2. Split automático del monto recibido (TrypoPMS + terceros)

## Scope del demo

- NO necesita ser bonito
- NO necesita frontend elaborado
- SÍ necesita validar que los endpoints responden correctamente
- SÍ necesita el flujo split funcionando end-to-end en test mode

## Flujo principal

```
Cliente paga
    → Checkout Session (Fintoc Widget)
    → Webhook payment_intent.succeeded recibido
    → Split: X% → TrypoPMS | Y% → tercero
    → Transfer v2 al account number del tercero
```

## Endpoints a validar

| Endpoint | Acción | Estado |
|---|---|---|
| `checkout_sessions` create | Generar link de pago | pendiente |
| `checkout_sessions` get | Verificar estado | pendiente |
| `payment_intents` list/get | Ver pagos recibidos | pendiente |
| `webhook_endpoints` create | Registrar listener | pendiente |
| `webhooks listen` | Recibir eventos local | pendiente |
| `trigger` payment_intent.succeeded | Simular pago exitoso | pendiente |
| `v2 transfers` create | Enviar split a tercero | pendiente |
| `v2 accounts` get | Ver balance post-split | pendiente |

## Split

- Porcentaje configurable por reserva
- TrypoPMS retiene su parte en `acc_3E8duZcU6ELPNeOUjoeaCOolKbj`
- El resto se transfiere via `v2 transfers create` al account number del tercero

## Integración con motor de reserva

El motor de reserva ya existe. El sistema de pagos se engancha via:
- `POST /webhook` → recibe evento de Fintoc → ejecuta split
- Reserva incluye: monto total, % split, account number del tercero

## Stack del demo

- Python (script simple, sin framework)
- ngrok o similar para exponer webhook local
- `.env` para credenciales

## Archivos

```
demo/
├── create_checkout.py    # crea checkout session
├── webhook_server.py     # recibe evento y ejecuta split
└── split.py              # lógica de split + transfer
```
