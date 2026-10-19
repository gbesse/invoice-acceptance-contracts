# Invoice Acceptance Contracts

[Français](README.md) · [English](README.en.md)

**Una factura puede circular correctamente y no respetar las condiciones de aceptación del comprador.**

El laboratorio concilia pedido, recepciones aceptadas, cantidades facturadas previamente y factura. Prepara una copia corregida con pruebas sin transmitir facturas, cambiar estados oficiales ni autorizar pagos.

![Conciliación sintética y propuesta de copia corregida](docs/preview-fr.png)

## Probar

Python 3.11 o posterior, solo biblioteca estándar.

```sh
python3 -m invoice_contract serve --lang es
```

Abrir `http://127.0.0.1:8768/?lang=es`. Diez unidades pedidas, tres recibidas y dos facturadas antes: **queda una unidad disponible**, mientras la factura solicita cuatro a precio incorrecto. La copia cambia el **subtotal de líneas de 50,80 a 12,50 EUR** y vuelve a conciliarse. No es un abono, factura emitida ni aprobación.

```sh
python3 -m invoice_contract audit invoice_contract/examples/partial-receipt.json
python3 -m invoice_contract prepare invoice_contract/examples/partial-receipt.json > propuesta.json
python3 -m invoice_contract verify-source invoice_contract/examples/partial-receipt.json propuesta.json
python3 -m invoice_contract import-ubl invoice_contract/examples/invoice.xml
```

`pip install .` proporciona `invoice-contract`. Interfaz, hallazgos y mensajes CLI en FR/EN/ES. `ready_for_review` solo indica ausencia de diferencias bajo el contrato proporcionado; sigue haciendo falta revisión.

## Contrato explícito y pruebas desconocidas

- Deben coincidir precio, unidad, divisa, artículo e identificadores tipados. Sin inventar conversiones ni equivalencias semánticas.
- `received` limita a recepción aceptada menos facturación previa y saldo del pedido. `ordered` expresa otro contrato sin exigir recepción.
- La recepción ausente permanece **desconocida**: ni entrega confirmada ni cero que permita corregir automáticamente.
- Pruebas repetidas idénticas no duplican cantidades; contenido contradictorio con igual identificador bloquea. Cada identificador representa una observación de línea, por ejemplo recepción + línea, única en ese contexto.
- Se agregan líneas de factura con una misma referencia y se envían a revisión; no pueden consumir cada una todo el saldo.
- Referencias sin resolver muestran candidatos SKU sin elegir. Historial por proveedor tipado + número de factura.

Cantidades y precios son cadenas decimales. Importes por línea con dos decimales y `ROUND_HALF_UP`, convención declarada del prototipo. No modela impuestos, abonos, anticipos complejos, cargos ni descuentos. Subtotal es suma de líneas, no total a pagar.

## Copia para revisar

`prepare` puede reducir una cantidad positiva al saldo probado, restaurar precio y recalcular importes. Los cambios citan pruebas. Conflictos de identidad, divisa, pruebas o referencias globales impiden una copia automática; las incógnitas siguen pendientes. Saldo cero requiere intervención humana.

SHA-256 vincula propuesta y caso inicial; `verify-source` detecta cambios de recepción o contrato. No prueba identidad ni autorización humana. No hay ejecutor remoto, pago ni llamada de producción.

## Importación UBL limitada y comparación

Lee espacios de nombres UBL `Invoice`, identificadores `schemeID`, pedido y [referencia de línea del comprador](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-OrderLineReference/cbc-LineID/). Rechaza DTD/entidades, monedas mezcladas, cargos/descuentos y cantidades base de precio distintas de uno. Adaptador pequeño: **ni validador UBL/Peppol completo ni lector Factur-X PDF/CII**. El XML de ejemplo no es una factura reglamentaria completa.

[ERPNext](https://docs.frappe.io/erpnext/purchase-invoice) ya relaciona compras/facturas con pedidos y recepciones. La hipótesis es un contrato autónomo, portable y explicable entre herramientas, no inventar conciliación. Las [especificaciones de factura electrónica](https://www.impots.gouv.fr/specifications-externes-b2b) ya cubren intercambio y estados; no se sustituyen. Sigue la corrección de nuestra investigación FE-MCP: demostrar valor de negocio más allá de circular estados.

## Validación y límites

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Catorce pruebas cubren evidencias, historial, cantidades compartidas, unidades/divisas, decimales e importación XML real. Navegador FR/EN/ES, copia, exportación, cambio de contrato y móvil; CI Python 3.11/3.12 y rueda fuera de fuentes. Salida 1 para diferencias/revisión o fuentes cambiadas; 2 para entrada no válida. Datos sintéticos: sin comprador, proveedor, asesor ni ERP real probado; sin validación fiscal ni superioridad SOTA. Licencia MIT; alfa de investigación.
