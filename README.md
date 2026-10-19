# Invoice Acceptance Contracts

[English](README.en.md) · [Español](README.es.md)

**Une facture peut circuler correctement tout en ne respectant pas ce que son acheteur peut accepter.**

Ce laboratoire rapproche une commande, ses réceptions acceptées, les quantités déjà facturées et une facture. Il prépare une copie corrigée avec ses preuves, sans transmettre de facture, changer de statut officiel ou autoriser un paiement.

![Rapprochement synthétique et proposition de copie corrigée](docs/preview-fr.png)

## Essayer

Python 3.11 ou supérieur, bibliothèque standard uniquement.

```sh
python3 -m invoice_contract serve --lang fr
```

Ouvrir `http://127.0.0.1:8768/?lang=fr`. La démonstration synthétique contient dix unités commandées, trois reçues et deux déjà facturées : il reste **une unité disponible**, tandis que la facture en demande quatre au mauvais prix. La copie proposée passe de **50,80 à 12,50 EUR de sous-total de lignes**, puis est rapprochée de nouveau. Ce n’est ni un avoir, ni une facture émise, ni une approbation.

```sh
python3 -m invoice_contract audit invoice_contract/examples/partial-receipt.json
python3 -m invoice_contract prepare invoice_contract/examples/partial-receipt.json > proposition.json
python3 -m invoice_contract verify-source invoice_contract/examples/partial-receipt.json proposition.json
python3 -m invoice_contract import-ubl invoice_contract/examples/invoice.xml
```

`pip install .` fournit aussi `invoice-contract`. UI, constats et messages CLI sont en FR/EN/ES. Le résultat `ready_for_review` signifie seulement qu’aucun écart n’a été trouvé dans le contrat fourni ; une revue reste nécessaire.

## Contrat explicite et preuves inconnues

- Le prix, l’unité, la devise, l’article et les identifiants typés doivent correspondre. Aucune conversion ni correspondance sémantique n’est inventée.
- La base `received` limite la quantité à la réception acceptée, moins la facturation antérieure, et au solde commandé. La base `ordered` représente un autre contrat et ne requiert pas la réception.
- Une réception absente reste **inconnue**. Elle ne devient ni une livraison certaine, ni une quantité nulle permettant une correction automatique.
- Des preuves répétées à l’identique ne doublent pas les quantités ; un même identifiant contradictoire bloque la préparation. L’identifiant d’une preuve désigne une observation de ligne, par exemple réception + ligne, et doit être unique dans ce contexte.
- Plusieurs lignes de facture sur la même ligne de commande sont agrégées et envoyées en revue. Elles ne reçoivent pas chacune le solde complet.
- Les références non résolues montrent les candidats par SKU, sans en choisir un. L’historique de factures est identifié par fournisseur typé + numéro de facture.

Les quantités et prix entrent comme chaînes décimales. Les montants de lignes sont arrondis à deux décimales selon `ROUND_HALF_UP`, convention déclarée de ce prototype. Les taxes, avoirs, acomptes complexes, frais et remises ne sont pas modélisés. Le sous-total désigne la somme des lignes, pas le montant total payable.

## Une copie à relire

`prepare` peut réduire une quantité positive au solde prouvé et rétablir le prix convenu, puis recalculer les montants. Les changements contiennent les références de preuve. Les identités, devises, conflits de preuves ou références globales incohérentes empêchent la copie automatique ; les inconnues restent à résoudre. Une quantité disponible nulle demande une intervention humaine.

Le digest SHA-256 lie la proposition au dossier initial ; `verify-source` détecte si la réception ou le contrat a changé entre-temps. Ce digest ne prouve ni l’identité, ni l’autorisation d’une personne. Le projet ne dispose d’aucun exécuteur distant, paiement ou appel de production.

## Import UBL limité et positionnement

L’importeur lit réellement les espaces de noms UBL `Invoice`, les identifiants avec `schemeID`, la référence de commande et la [référence de ligne acheteur](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-OrderLineReference/cbc-LineID/). Il refuse DTD/entités, devises monétaires mélangées, remises/charges et prix par quantité de base différente de un. C’est un petit adaptateur de lignes : **ni validateur UBL/Peppol complet, ni lecteur Factur-X PDF/CII**. Le XML fourni est une fixture de cet adaptateur, pas une facture réglementaire complète.

[ERPNext](https://docs.frappe.io/erpnext/purchase-invoice) propose déjà des achats/factures reliés aux commandes et réceptions. L’apport à tester ici est un contrat autonome, transportable et explicable entre outils, pas l’invention du rapprochement. Les [spécifications de facturation électronique](https://www.impots.gouv.fr/specifications-externes-b2b) couvrent déjà leurs échanges et statuts ; ce projet ne les remplace pas et reprend la correction de notre recherche FE-MCP : il faut démontrer un gain métier au-delà de la circulation des statuts.

## Validation et limites

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Quatorze tests couvrent preuves manquantes/contradictoires, historique, quantité partagée, unités/devises, décimales et vrai import XML. Navigateur FR/EN/ES, copie, export, changement de contrat et mobile ; CI Python 3.11/3.12 et roue hors sources. Code 1 pour écarts/revue ou source modifiée, 2 pour entrée non valide. Données synthétiques : aucun acheteur, fournisseur, cabinet ou ERP réel testé ; aucune validation fiscale ou supériorité SOTA. Licence MIT, alpha de recherche.
