# Test Mode — Fintoc

Fuente: https://docs.fintoc.com/docs/test-mode

## Cómo funciona

El modo test se activa simplemente usando las **keys de test** (`sk_test_`, `pk_test_`). No hay un switch separado — la key determina el ambiente.

## Test vs Live

| Aspecto | Test | Live |
|---|---|---|
| Keys | `sk_test_` / `pk_test_` | `sk_live_` / `pk_live_` |
| Objetos | Simulados | Reales |
| Cuentas bancarias | Cuentas de prueba | Cuentas reales de clientes |
| Transacciones | Sin movimiento real de dinero | Dinero y autorizaciones reales |

Los objetos de test y live están completamente aislados — datos de un ambiente no son accesibles desde el otro.

## Productos con soporte test

- Movements (Data Aggregation)
- Payment Initiation
- Direct Debit
- Transfers

## Credenciales de prueba

Para el Widget en modo test, Fintoc provee credenciales bancarias de prueba. Ver: https://docs.fintoc.com/docs/test-credentials

## CLI en modo test

```bash
# Todos los comandos operan en test si la key es sk_test_
fintoc login --api-key sk_test_...
fintoc payment_intents list   # lista payment intents de test

# Trigger de eventos de prueba
fintoc trigger payment_intent.succeeded
fintoc trigger payment_intent.succeeded --override amount=5000 --override currency=CLP

# Webhooks en tiempo real (test)
fintoc webhooks listen
fintoc webhooks listen --forward-to http://localhost:3000/webhooks
```
