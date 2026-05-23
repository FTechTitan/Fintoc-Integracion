# API Keys — Fintoc

Fuente: https://docs.fintoc.com/docs/api-keys

## Tipos de keys

Cada cuenta tiene **4 keys**:

| Tipo | Prefijo test | Prefijo live | Uso |
|---|---|---|---|
| Public key | `pk_test_` | `pk_live_` | Identificar la cuenta en el Widget (no sensible) |
| Secret key | `sk_test_` | `sk_live_` | Autenticar llamadas a la API (solo backend, sensible) |

- La **public key** solo se usa para inicializar el Widget en el frontend.
- La **secret key** debe usarse exclusivamente desde el backend. **Nunca exponer en frontend.**

## Acceso y gestión

- Dashboard: https://dashboard.fintoc.com/api-keys
- La live secret key **solo se muestra una vez** al activarla o rotarla. Guardarla de inmediato.
- Los ambientes test y live están completamente aislados — los recursos de uno no pueden usarse en el otro.

## Buenas prácticas

- Rotar keys al menos **una vez por año**.
- Habilitar **IP Restrictions** para aceptar requests solo desde IPs o bloques CIDR específicos.
  - Si se activa con lista vacía → **ningún request es aceptado**.
- Guardar en variables de entorno, nunca en el código.

## Uso en el CLI

```bash
# Login interactivo (guarda en ~/.fintoc/config.toml)
fintoc login

# Login no interactivo
fintoc login --api-key sk_test_...

# Override por comando
fintoc payment_intents list --api-key sk_test_...

# Variable de entorno
export FINTOC_API_KEY=sk_test_...
fintoc charges list
```

## Uso en la API directamente

```bash
curl https://api.fintoc.com/v1/payment_intents \
  -u sk_test_...:
```

El secreto va como username en Basic Auth (password vacío).
