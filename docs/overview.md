# Estructura de la Documentación Fintoc

Fuente: https://docs.fintoc.com | Versiones API: 2021-03-23, 2023-11-15, v2026-02-01

## Guides

### Conceptos generales
- Currencies → `/docs/currencies`
- API Keys → `/docs/api-keys`
- API rate limits → `/docs/api-rate-limits`
- Changes to the API → `/docs/changes`
- Test mode → `/docs/test-mode`
- Building with AI → `/docs/building-with-ai`
- SDKs e Integraciones → `/docs/sdks`

### Payments (Pagos)
- Overview y Quickstart
- Accept payments (one-time, recurring)
- Fintoc Collect (payouts, reembolsos, reconciliación)
- Direct Payments
- UX Guidelines (Chile, México)
- E-commerce Plugins: VTEX, Shopify, Magento
- Pagos en efectivo (México)
- BNPL - Buy Now Pay Later (Chile)

### Transfers (Transferencias)
- Entity, Account, Transfer (modelos de datos)
- Casos de uso: payins, payouts, wallets, nómina
- Inbound/Outbound Transfers
- Verificación CLABE
- Batch Transfers
- Gestión de cuentas (Account Numbers)

### Direct Debit (Débito Directo)
- Overview
- Integration flow
- Countries y instituciones soportadas
- Test integrations (simulaciones)

### Movements (Movimientos/Aggregation)
- Fiscal Links
- Refresh Intents
- Guías de integración
- Credenciales de prueba

### Webhooks
- Walkthrough
- Creación y activación de endpoints
- Validación de firma
- Testing
- Best practices

### Widget
- Web integration
- WebView (mobile)
- Event listeners

### Fintoc CLI
- Instalación y uso → `/docs/fintoc-cli`
- Keys y permisos

## API Reference

URL base: `https://docs.fintoc.com/reference/`

### Core
- Introducción y autenticación
- Error handling
- Idempotent requests
- Metadata
- Pagination

### Endpoints por producto

**Payments**
- Checkout Sessions (create, get, expire)
- Payment Intents (create, list, get)
- Payment Methods (create, list, get)
- Customers (create, list, get)
- Subscriptions (get, list)
- Charges (create, get, list, cancel)
- Refunds
- Payment Links
- Payouts

**Transfers v2**
- Accounts (create, get, list, update)
- Account Numbers (create, get, list, delete, update)
- Account Statements (list)
- Account Verifications (create, get, list)
- Entities (get, list)
- Movements (get, list)
- Transfers (create, get, list, returns)
- SPEI codes

**Data Aggregation**
- Links (get, list, update, delete)
- Link Intents
- Accounts (get, list)
- Movements (get, list)
- Refresh Intents (create)
- Invoices, Tax Returns, Tax Statements (Fiscal)

**Shared**
- Webhook Endpoints (create, get, list, delete, activate)
- Events (types)
- Institutions (list)

## Changelog destacado

- Apple Pay button para checkout en un click
- Múltiples API Keys por organización
- Lanzamiento del Fintoc CLI
- Monthly account statements
- CLABE search y delete

## SDKs oficiales

| Lenguaje | Repo |
|---|---|
| Python | https://github.com/fintoc-com/fintoc-python |
| Ruby | https://github.com/fintoc-com/fintoc-ruby |
| Node.js | https://github.com/fintoc-com/fintoc-node |
| Zapier | Integración nativa |
