const texts = {
  fr: {
    eyebrow: 'FACTURATION · AVANT LA TRANSMISSION',
    title: 'La facture circule.\nPeut-on l’accepter ?',
    lede: 'Une référence de commande ne suffit pas. Rapprochez réception, quantités déjà facturées et prix convenu ; préparez une copie corrigée, avec ses preuves.',
    context: 'Les faits de l’acheteur',
    receipt: 'Quantité reçue et acceptée',
    prior: 'Quantité déjà facturée',
    missing: 'La preuve de réception manque',
    basis: 'Base contractuelle de facturation',
    received: 'Quantité reçue',
    ordered: 'Quantité commandée',
    audit: 'Rapprocher les pièces →',
    local: 'Données synthétiques. Aucun fournisseur, ERP ou plateforme n’est contacté.',
    findings: 'Ce qui empêche l’acceptation',
    available: 'quantité disponible',
    billed: 'quantité facturée',
    net: 'sous-total HT · EUR',
    draft: 'Une proposition à relire',
    prepare: 'Préparer une copie corrigée',
    download: 'Exporter la proposition JSON',
    limits:
      'Contrat d’acceptation fourni par l’acheteur, sans validation fiscale, paiement ni modification de statut officiel. Les plateformes gèrent déjà la circulation des factures et statuts ; cet outil rapproche des faits métier. Aucun accès de production incwo ou autre ERP.',
    blocked: 'ÉCARTS BLOQUANTS',
    review: 'PREUVES À REVOIR',
    ready_for_review: 'PRÊT POUR REVUE',
    draft_ready_for_review: 'COPIE PRÊTE POUR REVUE',
    needs_context_review: 'CONTEXTE À REVOIR',
    needs_evidence_or_human_edit: 'PREUVES OU CORRECTION HUMAINE NÉCESSAIRES',
    unknown: 'inconnue',
    price_mismatch: 'Le prix diffère de la commande',
    quantity_exceeds_contract: 'La quantité dépasse le contrat disponible',
    missing_receipt_evidence: 'La réception n’est pas prouvée',
    line_total_mismatch: 'Le montant de ligne ne correspond pas',
    subtotal_mismatch: 'Le sous-total ne correspond pas',
    order_line_unresolved: 'La ligne de commande reste à identifier',
    unit_mismatch: 'Les unités diffèrent',
    receipt_unit_mismatch: 'Les unités de réception diffèrent',
    item_mismatch: 'Les articles diffèrent',
    buyer_mismatch: 'Les acheteurs diffèrent',
    seller_mismatch: 'Les fournisseurs diffèrent',
    currency_mismatch: 'Les devises diffèrent',
    order_reference_mismatch: 'La référence de commande diffère',
    invoice_seen_before: 'Cette facture figure déjà dans l’historique',
    conflicting_receipt_evidence: 'Les preuves de même identifiant se contredisent',
    unmapped_receipt: 'Une réception ne correspond à aucune ligne',
    prior_billing_exceeds_order: 'La facturation antérieure dépasse la commande',
    split_order_line_requires_review: 'Plusieurs lignes consomment la même référence',
    expected: 'Attendu',
    actual: 'Constaté',
    busy: 'Rapprochement en cours…',
    done: 'Pièces rapprochées. Aucune action externe.',
    error: 'Entrée non valide ou serveur indisponible.',
    quantity: 'quantité',
    unit_price: 'prix unitaire',
    before: 'Sous-total avant',
    after: 'Sous-total proposé',
    noAction: 'Aucun paiement, aucune transmission, aucune approbation.',
    noFindings: 'Aucun écart dans ce contrat ; une revue reste nécessaire.',
  },
  en: {
    eyebrow: 'INVOICING · BEFORE SUBMISSION',
    title: 'The invoice moves.\nCan it be accepted?',
    lede: 'An order reference is not enough. Reconcile receipts, prior billed quantities and agreed prices; prepare an evidence-backed corrected copy.',
    context: 'The buyer’s facts',
    receipt: 'Received and accepted quantity',
    prior: 'Previously billed quantity',
    missing: 'Receipt evidence is missing',
    basis: 'Contractual billing basis',
    received: 'Received quantity',
    ordered: 'Ordered quantity',
    audit: 'Reconcile the evidence →',
    local: 'Synthetic data. No supplier, ERP or platform is contacted.',
    findings: 'What prevents acceptance',
    available: 'available quantity',
    billed: 'billed quantity',
    net: 'net line subtotal · EUR',
    draft: 'A proposal to review',
    prepare: 'Prepare a corrected copy',
    download: 'Export JSON proposal',
    limits:
      'Buyer-supplied acceptance contract, without tax validation, payment or official-status mutation. Platforms already handle invoice/status circulation; this tool reconciles business facts. No production incwo or other ERP access.',
    blocked: 'BLOCKING DISCREPANCIES',
    review: 'EVIDENCE NEEDS REVIEW',
    ready_for_review: 'READY FOR REVIEW',
    draft_ready_for_review: 'COPY READY FOR REVIEW',
    needs_context_review: 'CONTEXT NEEDS REVIEW',
    needs_evidence_or_human_edit: 'EVIDENCE OR HUMAN EDIT REQUIRED',
    unknown: 'unknown',
    price_mismatch: 'Price differs from the order',
    quantity_exceeds_contract: 'Quantity exceeds remaining contract capacity',
    missing_receipt_evidence: 'Receipt is not evidenced',
    line_total_mismatch: 'Line amount does not match',
    subtotal_mismatch: 'Subtotal does not match',
    order_line_unresolved: 'Order line remains unresolved',
    unit_mismatch: 'Units differ',
    receipt_unit_mismatch: 'Receipt units differ',
    item_mismatch: 'Items differ',
    buyer_mismatch: 'Buyers differ',
    seller_mismatch: 'Suppliers differ',
    currency_mismatch: 'Currencies differ',
    order_reference_mismatch: 'Order reference differs',
    invoice_seen_before: 'Invoice already appears in history',
    conflicting_receipt_evidence: 'Evidence with the same identifier conflicts',
    unmapped_receipt: 'Receipt has no matching order line',
    prior_billing_exceeds_order: 'Prior billing exceeds the order',
    split_order_line_requires_review: 'Multiple lines consume one order reference',
    expected: 'Expected',
    actual: 'Actual',
    busy: 'Reconciling…',
    done: 'Evidence reconciled. No external action.',
    error: 'Invalid input or server unavailable.',
    quantity: 'quantity',
    unit_price: 'unit price',
    before: 'Subtotal before',
    after: 'Proposed subtotal',
    noAction: 'No payment, submission or approval.',
    noFindings: 'No discrepancy under this contract; review remains necessary.',
  },
  es: {
    eyebrow: 'FACTURACIÓN · ANTES DEL ENVÍO',
    title: 'La factura circula.\n¿Se puede aceptar?',
    lede: 'Una referencia de pedido no basta. Concilia recepciones, cantidades ya facturadas y precios acordados; prepara una copia corregida con pruebas.',
    context: 'Los hechos del comprador',
    receipt: 'Cantidad recibida y aceptada',
    prior: 'Cantidad ya facturada',
    missing: 'Falta prueba de recepción',
    basis: 'Base contractual de facturación',
    received: 'Cantidad recibida',
    ordered: 'Cantidad pedida',
    audit: 'Conciliar las pruebas →',
    local: 'Datos sintéticos. Sin contactar proveedores, ERP ni plataformas.',
    findings: 'Qué impide la aceptación',
    available: 'cantidad disponible',
    billed: 'cantidad facturada',
    net: 'subtotal neto · EUR',
    draft: 'Una propuesta que revisar',
    prepare: 'Preparar copia corregida',
    download: 'Exportar propuesta JSON',
    limits:
      'Contrato de aceptación del comprador, sin validación fiscal, pago ni modificación de estados oficiales. Las plataformas ya gestionan circulación de facturas y estados; esta herramienta concilia hechos de negocio. Sin acceso de producción incwo ni otros ERP.',
    blocked: 'DIFERENCIAS BLOQUEANTES',
    review: 'PRUEBAS POR REVISAR',
    ready_for_review: 'LISTO PARA REVISIÓN',
    draft_ready_for_review: 'COPIA LISTA PARA REVISIÓN',
    needs_context_review: 'CONTEXTO POR REVISAR',
    needs_evidence_or_human_edit: 'SE REQUIEREN PRUEBAS O EDICIÓN HUMANA',
    unknown: 'desconocida',
    price_mismatch: 'El precio difiere del pedido',
    quantity_exceeds_contract: 'La cantidad supera la capacidad contractual restante',
    missing_receipt_evidence: 'La recepción no está probada',
    line_total_mismatch: 'El importe de línea no coincide',
    subtotal_mismatch: 'El subtotal no coincide',
    order_line_unresolved: 'Falta identificar la línea de pedido',
    unit_mismatch: 'Las unidades difieren',
    receipt_unit_mismatch: 'Las unidades de recepción difieren',
    item_mismatch: 'Los artículos difieren',
    buyer_mismatch: 'Los compradores difieren',
    seller_mismatch: 'Los proveedores difieren',
    currency_mismatch: 'Las divisas difieren',
    order_reference_mismatch: 'Difiere la referencia de pedido',
    invoice_seen_before: 'La factura ya figura en el historial',
    conflicting_receipt_evidence: 'Pruebas con igual identificador se contradicen',
    unmapped_receipt: 'La recepción no corresponde a una línea',
    prior_billing_exceeds_order: 'La facturación previa supera el pedido',
    split_order_line_requires_review: 'Varias líneas consumen una referencia',
    expected: 'Esperado',
    actual: 'Observado',
    busy: 'Conciliando…',
    done: 'Pruebas conciliadas. Sin acción externa.',
    error: 'Entrada no válida o servidor no disponible.',
    quantity: 'cantidad',
    unit_price: 'precio unitario',
    before: 'Subtotal anterior',
    after: 'Subtotal propuesto',
    noAction: 'Sin pago, transmisión ni aprobación.',
    noFindings: 'Sin diferencias bajo este contrato; sigue siendo necesaria la revisión.',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  m = texts[lang] || texts.en;
document.documentElement.lang = texts[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((x) => (x.textContent = m[x.dataset.i18n]));
document.querySelectorAll('nav a').forEach((a) => {
  if (a.textContent.toLowerCase() === document.documentElement.lang)
    a.setAttribute('aria-current', 'page');
});
for (const option of document.querySelector('#basis').options) option.textContent = m[option.value];
const $ = (id) => document.getElementById(id),
  el = (tag, text, cls) => {
    const x = document.createElement(tag);
    if (text !== undefined) x.textContent = text;
    if (cls) x.className = cls;
    return x;
  };
let original, caseData, proposal;
function current() {
  const c = structuredClone(original);
  c.order.lines[0].previous_billed_quantity = $('prior').value;
  c.order.lines[0].billing_basis = $('basis').value;
  if ($('missing').checked) c.receipts = [];
  else c.receipts[0].quantity = $('receipt').value;
  return c;
}
function render(report) {
  $('verdict').textContent = m[report.status];
  $('available').textContent = report.lines[0].permitted_quantity ?? m.unknown;
  $('digest').textContent = report.snapshot_sha256;
  $('findings').replaceChildren();
  for (const f of report.findings) {
    const box = el('div', undefined, 'finding');
    box.append(el('h3', m[f.code] || f.code));
    if (f.expected !== null)
      box.append(
        el(
          'p',
          `${m.expected}: ${typeof f.expected === 'object' ? JSON.stringify(f.expected) : f.expected} · ${m.actual}: ${f.actual}`,
        ),
      );
    box.append(el('code', f.sources.join(' · ')));
    $('findings').append(box);
  }
  if (!report.findings.length) $('findings').append(el('p', m.noFindings, 'hint'));
  $('status').textContent = m.done;
}
async function audit() {
  $('audit').disabled = true;
  $('status').textContent = m.busy;
  proposal = null;
  $('proposal').replaceChildren();
  try {
    caseData = current();
    const response = await fetch('/api/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!response.ok) throw Error();
    render(await response.json());
  } catch {
    $('status').textContent = m.error;
  } finally {
    $('audit').disabled = false;
  }
}
async function prepare() {
  $('prepare').disabled = true;
  try {
    caseData = current();
    const response = await fetch('/api/prepare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!response.ok) throw Error();
    proposal = await response.json();
    $('proposal').replaceChildren();
    $('proposal').append(el('strong', m[proposal.status], 'proposal-status'));
    for (const c of proposal.changes) {
      const row = el('div', undefined, 'change');
      row.append(el('span', m[c.field]), el('span', `${c.before} → ${c.after}`));
      $('proposal').append(row);
    }
    if (proposal.after_line_subtotal)
      $('proposal').append(
        el(
          'p',
          `${m.before}: ${proposal.before_line_subtotal} · ${m.after}: ${proposal.after_line_subtotal}`,
          'hint',
        ),
      );
    $('proposal').append(el('p', m.noAction, 'hint'));
  } catch {
    $('status').textContent = m.error;
  } finally {
    $('prepare').disabled = false;
  }
}
$('audit').addEventListener('click', audit);
$('prepare').addEventListener('click', prepare);
$('download').addEventListener('click', () => {
  if (!proposal) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(proposal, null, 2)], { type: 'application/json' }),
    ),
    a = el('a');
  a.href = url;
  a.download = 'invoice-acceptance-proposal.json';
  a.click();
  URL.revokeObjectURL(url);
});
try {
  const response = await fetch('/api/example');
  if (!response.ok) throw Error();
  original = await response.json();
  await audit();
} catch {
  $('status').textContent = m.error;
}
