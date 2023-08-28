import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_blue_white_collar(job_desc):
    blue_or_white_collar_prompt = """
        Definition of a blue-collar worker: blue-collar workers are typically involved in manual or labor-intensive tasks that require physical effort and skill. They are often employed in industries such as manufacturing, construction, agriculture, mining, transportation, and maintenance. The work of blue-collar employees may involve operating machinery, assembling products, performing manual labor, and working in environments that might be physically demanding or hazardous. 
        Definition of a white-collar worker: White-collar workers are typically associated with professional, administrative, managerial, and office-based roles. They often work in sectors such as finance, information technology, healthcare, education, marketing, and various corporate settings. White-collar jobs tend to involve tasks that are more knowledge-based, involve decision-making, and may require skills such as communication, analysis, problem-solving, and coordination

        If the job description written in Czech langauge below describes a blue collar position ouput "blue" and if white collar position ouput "white".

        job description: \"\"\"
            {}
        \"\"\"
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=blue_or_white_collar_prompt.format(job_desc),
        max_tokens=1024,
        temperature=0.5
    ).choices[0].text.strip().lower()

    if "bl" in response: return "blue"
    elif "wh" in response: return "white"


def classify_is_client_facing(job_desc):
    is_client_facing_prompt = """
        Is the job description written in Czech langauge below describes a position that is customer-facing? A customer-facing position is one where you work directly with customers, helping them with their needs, questions, or concerns. If it is a customer-facing position output "customer-facing", and output "internal-facing" if it's not a customer-facing position.

        job description: \"\"\"
            {}
        \"\"\"
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=is_client_facing_prompt.format(job_desc),
        max_tokens=1024,
        temperature=0.5
    ).choices[0].text.strip().lower()

    if "cust" in response:
        return "customer-facing"
    elif "int" in response:
        return "internal-facing"


def generate_job_experiences(job_description, number_of_experiences):
    experience_prompt = """
    Přečti následující úryvek z pracovní nabídky:
    {}


    Vygeneruj {} pracovní zkušenosti ze stejného odvětní jako je výše uvedená praocovní nabídka. Použij reálné názvy firem. Text bude následně použit v životopisu. Nečísluj vygenerované pracovní zkušenosti.

    Formát jedné prcovní zkušenosti:
    <h3><název firmy></h3>
    <b><datum začátku a datum konce></b>
    <p><popis náplňě práce></p>
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=experience_prompt.format(job_description, str(number_of_experiences)),
        max_tokens=1024,
        temperature=0.9
    ).choices[0].text

    return response

def generate_education(job_description, education_type):
    experience_prompt = """
    Přečti následující úryvek z pracovní nabídky:
    {}
    
    Vygeneruj záznam o vzdělání dosaženém na {} z podobného oboru jako je výše uvedená pracovní nabídka. Použij reálné názvy škol. Text bude následně použit v životopisu.

    Formát jedné prcovní zkušenosti:
    <h3><název školy></h3>
    <b><datum začátku a datum konce></b>
    <p><obor školy></p>
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=experience_prompt.format(job_description, education_type),
        max_tokens=1024,
        temperature=0.9
    ).choices[0].text

    return response

desc1 = "Hledáme Kurýry, kteří budou chtít vozit nákupy našim skvělým zákazníkům.Jezdit můžete klidně pouze jeden den v týdnu ......Vše záleží jen na vás :)Fakturace?u nás si můžete své peníze za rozvezené zakázky vybrat hned následující den.průměrná fakturace až 3.800,-Kč denně! veškerá dýška jsou vaše!Vyberte si sklad ze kterého chcete rozvážet:LibocChrášťanyHorní PočerniceČím rozvážet?naším autem (výhodně vám ho pronajmeme)pronajaté vozidlo můžete využívat na cestu domu a do práce, v případě navazujících zakázkových blokůKterý den a jak dlouho za volantem?....to záleží čistě na Vás! V naší aplikaci si vybere každý, máme neomezené možnostiPro spolupráci potřebujete?IČOčistý TRřidičské oprávnění...min. 1 rokA víte co? Přijďte si to vyzkoušet!odpovězte na nabídkumy se vám ozveme a domluvíme si schůzkuv rámci schůzky si zkusíte jízdu s Kurýrempopovídáte si, navštívíte naše společné zákazníky a vy zjistíte, že být Kurýrem a vozit nákupy pro Rohlík je super :)pokud si plácneme a vás"
desc2 = "Máte talent opravit všechno, co se Vám dostane pod ruce?Zvládáte více věci najednou a chcete pořádnou výzvu?Tým mechaniků – seřizovačů hledá nové kolegy!!Co bude Vaším denním chlebem:Údržba strojů ve výrobním areálu.Provádění písemných záznamů oprav.Samostatné řízení oprav, a to těch náhlých.Preventivní kontrola na pracovištích.Vyžadujeme:Ochotu se učit – vše Vás naučíme.Chuť přinášet vlastní řešení.Vyučení v oboru bude pro Vás výhodou.Ochotu pracovat ve směnném režimu (12h směny).A proč pracovat v Kavalierglass?Profesionální přístup a odborné zaškolení v době adaptace.Nabízíme velké možnosti seberealizace a oblasti inovací a vychytávek.Odpovídající mzdové ohodnocení.Motivační odměny závislé na výkonu zaměstnance i odměny závislé na výsledcích celé společnosti.Možnosti dalšího vzdělávání.5 týdnů dovolené.Práci na směny a s ní spojené nadstandardní příplatky (2000 Kč za docházku)Stravování v areálu závodu s nízkou cenou obědů, výhodný mobilní tarif pro celou Vaši rodinu"
desc3 = "Jste technický typ, co si umí poradit v jakékoliv situaci?Hledáte uplatnění svých zkušeností a znalostí při výrobě krásných produktů?Rozšiřujeme výrobu tak pojďte pracovat k nám!!Co bude výsledkem Vaší práce u nás?Plynulá a bezproblémová obsluha strojního zařízení pro výrobu sklářských výrobků.Systémová kontrola výrobních procesů.Minimalizovat výrobu neshodných výrobků a škody vznikajících na zařízeních.Preventivní i periodická údržba zařízení.Vyžadujeme:Zodpovědný přistup k zadané práci.Chuť pracovat a učit se novým věcem.Dodržování všech bezpečnostních opatření na pracovišti.Kontrolu případných nedostatků na stroji či na tavené hmotě a následně jejich hlášení směnovému technologovi.Co Vám můžeme na oplátku nabídnout?Hmatatelné výsledky Vaší práce. A věřte, že vyrábíme skutečně krásné produkty !!Profesionální přístup a v době adaptace (naši zaměstnanci jsou pro nás prioritou) !!Odborné zaškolení (účastníte se školy práce, kde Vás vše postupně naučíme) !!Stabilní a pers"

##print(generate_education(desc3, "vysoké škole"))