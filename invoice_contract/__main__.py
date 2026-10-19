import json
from pathlib import Path
import sys

from .engine import audit,prepare,digest
from .ubl import parse_invoice

ROOT=Path(__file__).resolve().parent
MESSAGES={"fr":{"help":"Utilisation : python -m invoice_contract demo|audit dossier.json|prepare dossier.json|import-ubl facture.xml|verify-source dossier.json proposition.json|serve [port] [--lang fr|en|es]","error":"Entrée non valide","ready":"Laboratoire de rapprochement local"},"en":{"help":"Usage: python -m invoice_contract demo|audit case.json|prepare case.json|import-ubl invoice.xml|verify-source case.json proposal.json|serve [port] [--lang fr|en|es]","error":"Invalid input","ready":"Local reconciliation laboratory"},"es":{"help":"Uso: python -m invoice_contract demo|audit caso.json|prepare caso.json|import-ubl factura.xml|verify-source caso.json propuesta.json|serve [puerto] [--lang fr|en|es]","error":"Entrada no válida","ready":"Laboratorio de conciliación local"}}


def example():return json.loads((ROOT/"examples/partial-receipt.json").read_text())


def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang="en"
    try:
        if "--lang" in args:
            i=args.index("--lang");lang=args[i+1];del args[i:i+2]
        if lang not in MESSAGES:raise ValueError("invalid_language")
        if not args or args[0] in ("help","--help"):print(MESSAGES[lang]["help"]);return 0
        command=args.pop(0)
        if command=="demo":result={"audit":audit(example()),"proposal":prepare(example())}
        elif command=="audit" and len(args)==1:result=audit(json.loads(Path(args[0]).read_text()))
        elif command=="prepare" and len(args)==1:result=prepare(json.loads(Path(args[0]).read_text()))
        elif command=="import-ubl" and len(args)==1:result=parse_invoice(Path(args[0]).read_bytes())
        elif command=="verify-source" and len(args)==2:
            case=json.loads(Path(args[0]).read_text());proposal=json.loads(Path(args[1]).read_text());result={"source_unchanged":digest(case)==proposal["snapshot_sha256"],"authorization_proven":False}
        elif command=="serve":
            from .server import serve
            port=int(args[0]) if args else 8768;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        else:raise ValueError("invalid_command")
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result.get("status") in ("blocked","review","needs_context_review","needs_evidence_or_human_edit") or result.get("source_unchanged") is False else 0
    except (ValueError,TypeError,KeyError,IndexError,OSError):
        message=MESSAGES.get(lang,MESSAGES["en"])["error"];print(json.dumps({"error":"invalid_input","message":message}),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
