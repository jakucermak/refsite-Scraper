import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models.post import Post
from src.psql.db import Base
from src.services.db_writer import create_tag_obj


@pytest.fixture
def html_page():
    html_content = """<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title>
    Title
    </title>
</head>
<body>
<section class="main">
    <div class="content flex">
        <div class="box12 maincontent">
            <article class="item" onclick="document.location='/cz/ekis/i-ekis/180550'">
            </article>
            <article class="item" onclick="document.location='/cz/ekis/i-ekis/180453'">
            </article>
            <article class="item" onclick="document.location='/cz/ekis/i-ekis/180457'">
            </article>
            <div class="pager">
                <span class="active"> 1 </span>
                <span class="delimiter"> | </span>
                <a href="/cz2/ekis/i-ekis">2</a>
                <span class="delimiter"> | </span>
                <a href="/cz3/ekis/i-ekis">3</a>
                <span class="delimiter"> | </span>
                <a href="/cz4/ekis/i-ekis">4</a>
                <span class="delimiter"> | </span>
                <span class="dots">  .. </span>
                <span class="delimiter"> | </span>
                <a href="/cz492/ekis/i-ekis">492</a>
                <span class="delimiter"> | </span>
                <a href="/cz2/ekis/i-ekis">»</a>
            </div>
        </div>
    </div>
</section>
</body>
</html>
"""
    yield [line.strip() for line in html_content.splitlines()]


@pytest.fixture()
def answer_text():
    text = """Dobrý den,

Energeticky úsporná opatření rodinných domů podporuje dotační titul „NZÚ rodinné domy“.
Podporována jsou opatření, která splňují dotační podmínky a byla realizována a uhrazena po 1. lednu 2021.

Z dotačního titulu „NZÚ rodinné domy“ lze získat dotace na :
- zateplení a výměnu otvorových výplní n (venkovních oken a dveří) - a to jako podporu dílčí, základní nebo optimální - dle celkového rozsahu a dosažené úspory energie
- výměnu zdroje tepla vytápění
- přípravu teplé užitkové vody
- fotovoltaické systémy
- systém řízeného větrání,
- využití tepla z odpadní vody,
- hospodaření s dešťovou a odpadní vodou,
- instalaci stínicí techniky,
- zelenou střechu,
- nabíjecí stanice pro elektromobil)

V případě kombinace výše uvedených (touto výzvou podporovaných) energeticky úsporných opatření je možnost získání dotačních bonusů.
Žádosti k této aktualizované výzvě jsou přijímány od konce září 2023.
Detailní podmínky pro získání této dotace jsou uvedeny v pokynech „NZÚ RD Závazné pokyny“ .

Dotační žádost se podává elektronickou formou a je nutno doložit požadované podklady. K žádosti je potřeba doložit souhlas případných spolumajitelů rodinného domu.

Pro získání dotace na zateplení (a výměnu oken, dveří a zasklení v obálce budovy) z dotačního titulu NZÚ Rodinné domy musí navržená a provedená energeticky úsporná opatření splnit
- minimální předepsané tepelně izolační parametry
- předepsanou výpočtovou úsporu dodané a neobnovitelné energie ve výši min. 10 % (dokládá se protokolem o výpočtu energetické náročnosti - detailněji viz. dotační podmínky).
Požadovaná úspora energie se v žádosti dokladuje
- v předepsaném formátu odborného posudku autorizovaným projektem zateplení (včetně případné výměny oken a dveří)
- a průkazem energetické náročnosti současného stavu budovy
- a průkazem energetické náročnosti stavu budovy s provedenými opatřeními.

Po realizaci se provedení energeticky úsporných opatření dokládá
- předepsaným rozsahem dokladů o dodaných materiálech, technických zařízení a vynaložených nákladech
- a předepsaným rozsahem odborného posudku s potvrzením odborného technického dozoru o provedení dle potvrzeného projektu.
Obsah a rozsah odborného posudku pro jednotlivé druhy energeticky úsporných opatření je konkrétně uveden v dotačních podmínkách NZÚ Rodinné domy.

Podmínky získání dotace pro případnou výměnu zdroje tepla za tepelné čerpadlo jsou podrobně popsány v dotčené části podmínek dotace NZÚ - jsou zde uvedeny požadované technické parametry a doklady, stejně jako obsah odborného posudku k těmto položkám, který nutno přiložit.

Dotací je možno získat 50 % nákladů na zateplení a výměnu otvorových výplní ( max až 950 tis Kč na dům), na ostatní položky lze obdržet příspěvky dle dotačního ceníku, celkově do 50 % doložených vynaložených nákladů, včetně nákladů na odborný posudek a projektovou přípravu (ve výši dle druhu zvolených energeticky úsporných opatření). .

Doporučení - pro předběžné stanovení a posouzení přínosu úspor zateplení, výměny oken a dalších případných energeticky úsporných opatření je vhodné využít možnost bezplatného zpravování návrhu energetických úspor pro Váš dům (tzv. NEO) a to formou poradenství M-EKIS.
To může zahrnout uvedené konzultace typu „návrh energetických opatření“ (NEO) - a to na základě žádosti o vypracování (vypracování je zdarma).

Prostřednictvím EKIS je tedy možno u mě (nebo u jiného zvoleného specialisty Ekis) zadat zdarma vypracovat resp. předběžně posoudit možnosti a doporučení energetických opatření pro orientaci při rozhodování o realizaci.
(Tento návrh energetických opatření NEO však nenahrazuje odborný (energetický) posudek. Zvýší však Vaši informovanost pro rozhodování o účelném rozsahu zateplení a energeticky úsporných opatření.)

Pro vypracování přesného energetického posouzení výchozího stávajícího stavu formou průkazu energetické náročnosti budovy (PENB) je obecně nutno provést detailní obhlídku, průzkum stavebních konstrukcí, průzkum stavebně technické infrastruktury a celkové rozměrové zaměření domu (pasportizaci), zejména teplosměnné obálky.
Rozsah potřebného zaměření a průzkumů pro vypracování tohoto PENB je dán velikostí a členitostí domu a jeho zařízení a zejména faktem, zda je k dispozici použitelná platná projektová dokumentace Vašeho domu. Zpracování průkazu energetické náročnosti budovy PENB pro stávající stav dle stávající legislativy obsahuje také návrh energeticky úsporných opatření, který může být dobrým vodítkem pro upřesnění rozhodování o rozsahu přípravy a realizace energeticky úsporných opatření.

Detailněji možno po dohodě řešit konzultací s nahlédnutím do Vašich dostupných projektů a podkladů a s případnou obhlídkou Vašeho domu, místo a čas dohodou.


S přáním hezkého dne Ing. Jiří Flašar, M-Ekis, ES MPO 1410"""
    yield text


@pytest.fixture()
def question_text():
    text = """Dobrý den, chtěla jsem se zeptat ohledně dotací . Budeme dělat tepelné čerpadlo, nová okna a vchodové dveře a chtěli bychom zjistit, jestli by se nám vyplatilo zažádat o dotace. Vás mi to našlo pod zelená úsporám jako specialistu, který by nám s tím mohl poradit. Je to tak? Děkuji Krmelová"""
    yield text


db = factories.postgresql_proc(port=1033, dbname="tests")


@pytest.fixture(scope="function")
def db_session(db):
    pg_host = db.host
    pg_port = db.port
    pg_user = db.user
    pg_password = db.password
    pg_db = db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, db.version, pg_password):
        connection_string = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_string)
        session = scoped_session(sessionmaker())
        session.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all(bind=engine)

        yield session
        session.close()


@pytest.fixture()
def tags():
    tags = ["tag1", "tag2"]
    return tags


@pytest.fixture()
def stored_tags(db_session, tags):
    tags_objects = []
    for tag in tags:
        tags_objects.append(create_tag_obj(db_session, tag))

    db_session.add_all(tags_objects)
    db_session.commit()


@pytest.fixture()
def tag3():
    yield "tag3"


@pytest.fixture()
def tag4():
    yield "tag4"


@pytest.fixture()
def tag5():
    yield "tag5"


@pytest.fixture()
def post1():
    post = Post(id=1, question="What is your favorite", answer="This and that!")
    yield post


@pytest.fixture()
def post2():
    post = Post(id=2, question="Your favourite music artist, what is",
                answer="Figrin D’an and the Modal Nodes, Master Yoda")
    yield post
