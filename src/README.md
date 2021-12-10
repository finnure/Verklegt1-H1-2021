# Kóðinn

Hérna er allur kóðinn geymdur

## Lýsing á forritinu

### Main

main.py er aðal forritið. Það er mjög einfalt, býr til instance af UI Handler og er með eina while lykkju sem kallar í start() á UI Handler þangað til notandi velur Q til að hætta.
Eina tilfellið sem keyrslan fer úr UI Handler og main kallar aftur í start() er ef notandi loggar sig út.

### UI Handler

uihandler.py er heilinn á bakvið forritið. Við upphaf keyrslu sér hann um að búa til tilvik af eftirfarandi klösum

- LlApi = Logic Layer API sem er tengingin frá View Layer við Logic Layer.
- Screen = Wrapper klasi utan um curses viðbótina.
- Allir view klasar fyrir mismunandi virkni í kerfinu

Allir view klasarnir fá tilvik af LlApi og Screen.  
start() byrjar á því að kalla í get_input() á LoginView. Notandi þarf að slá inn 3ja stafa id til að skrá sig inn.  
Næst er kallað í ViewFrame til að teikna rammann sem er alltaf sýnilegur í forritinu. Í rammanum eru listaðir
upp valmöguleikar sem eru alltaf aðgengilegir í kerfinu. Það er alltaf hægt að fara beina leið í menu á
flestum view klösum (listi í header) ásamt því að Home, Back, Login og Quit (listi í footer) eru í boði.  
Að lokum er MainMenu birtur og notandi getur byrjað að velja aðgerðir.

Hver valmöguleiki í kerfinu er með token sem notað er til að finna view_handler til að birta upplýsingar
sem beðið var um. Þetta token er samsett úr tveim strengjum með tvípunkt á milli. Fyrri hlutinn (view_key) segir til
um hvaða view klasi á aðgerðina sem kallað var í. Seinni hlutinn (handler_key) er vísun í aðgerð á view klasanum.

Til að koma í veg fyrir að stafsetningavillur valdi því að ekki nái tenging við rétt view er notast við klasa sem
geyma token sem fasta. Hver view klasi á sinn fasta klasa sem inniheldur þær aðgerðir sem hann býður uppá.
Þessir klasar og fastar eru skilgreindir í `ui/constants.py`

#### Breytur

`view_map` er dict með key sem passar við alla view_key möguleika. Value er vísun í tilvik af þeim view klasa sem sér um viðkomandi view_key.  
`SELF` er sérstakt tilvik af view_key sem passar ekki við fyrri lýsingu og er notað fyrir Back, Quit og Logout aðgerðirnar.  
`breadcrumb` er listi sem heldur utan um þær aðgerðir sem notandi hefur farið í gegnum og er notaður til að
fara til baka ef Back möguleikinn er notaður. Ef einhver af global valmöguleikunum er valinn er breadcrumb tæmdur.  
`current_view` geymir token sem segir til um hvaða view er virkt hverju sinni.

#### Aðgerðir

##### Private

`__init_views` býr til tilvik af öllum view klösum og setur upp view_map sem tengir view_key við view klasa.  
`__init_colors` forstillir alla liti sem eru notaðir í forritinu.  
`__init_menu` býr til tvö tilvik af Menu klasanum, eitt fyrir global valmöguleika í header og annað fyrir
global valmöguleika í footer. Þessi Menu tilvik eru send í ViewFrame til að birta réttar upplýsingar í rammanum.

##### Public

`start` sér um aðal virknina í forritinu, biður notanda um að velja option og finnur handler fyrir það sem var valið.  
`quit` sér um að færa stillingar sem curses notar til baka í fyrra horf til að terminal virki rétt eftir að keyrslu lýkur.  
`find_handler` notað fyrir aðgerðir samnýttar af mörgum klösum, eins og paging fyrir töflur og Back möguleiki sem view klasar geta kallað í til að fara til baka í það view sem kallaði í þá. view_key `GLOBAL` kallar í `find_handler`
`find_connection` splittar token í view_key og handler_key og sækir view klasa úr view_map. Ef view_key
er til staðar í view_map þá er kallað í `find_handler` aðgerðina á þeim view klasa sem á viðkomandi view_key
og handler_key sendur með.

### LlApi

API sem gerir allar aðgerðir í Logic Layer aðgengilegar. Þegar UI Handler býr til tilvik af LlApi sér hann um að búa til tilvik af DlApi og býr svo til tilvik af öllum Logic klösum og sendir þeim tilvik af dlapi.

Allar aðgerðir sem View Layer kallar í á Logic Layer fara í gegnum llapi yfir í viðeigandi Logic klasa sem sér um að sækja gögn og vinna flóknar aðgerðir á gögnunum.

### DlApi

API sem gerir allar aðgerðir í Data Layer aðgengilegar. Þegar LlApi býr til tilvik af dlapi þá býr hann til tilvik af öllum Data klösum sem sjá um að sækja og skrifa gögn í csv skrár.

Allar aðgerðir sem Logic Layer kallar í sem krefjast þess að sækja eða senda gögn í csv fara í gegnum dlapi sem sendir fyrirspurnina áfram í viðeigandi data klasa.

### Utils

Validation, síunar fastar fyrir inntak frá notanda og nokkrar hjálpar aðgerðir eru gerðar aðgengilegar í utils. Meðal annars eru aðgerðir tengdar dagsetningum, til að finna út hvort dagsetning sé innan valins ramma og til að sækja núverandi dagsetningu, svo dæmi séu tekin.

## UI

Allur kóði fyrir View Layer er í ui möppunni

Screen klasinn sem sér um aðgerðir sem birta texta og tákn á skjánum og tekur við input frá notanda er skjalaður í [Readme.md](ui/Readme.md) í ui möppunni.

Hver view klasi er með public aðgerðina `find_handler` sem UI Handler kallar í þegar valin aðgerð á heima í viðkomandi view. UI Handler sendir handler_key í find_handler, sem er notaður til að fletta upp í `__input_map` dict sem tengir handler_key við ákveðið view.

Hver view handler er með afmarkað hlutverk. Breytur sem þarf að senda í view eru geymdar á LlApi klasanum. View sem kallar þarf að passa uppá það að vista upplýsingarnar sem móttakandi view þarf að nota á réttum stað. `get_param` og `set_param` á LlApi eru notuð fyrir þetta, og fastar í constants.py tryggja að sami lykill er notaður á báðum endum.

Þegar view handler hefur lokið að birta sínar upplýsingar sendir hann þá valmöguleika sem eru í boði til baka í UI Handler sem tekur við þeim og reynir að tengja innslátt frá notanda við rétt view. Ef view sendir option sem streng til baka þá þarf það að vera token, og er það notað til að kalla beint í næsta view sem á að birtast án þess að notandi þurfi að velja það. Oftast eru option send sem dict þar sem valmöguleikinn er key og token er value.

## BL

Business logic er í bl möppunni

## DL

Data/Storage layer er í dl möppunni

Gögn í kerfinu eru geymd í csv skrám. csv.DictReader er notað til að lesa gögn beint í dict og til að hægt sé að senda dict til að skrifa í skrárnar.

Klasinn FileHandler er með þær aðgerðir sem eru notaðar til að eiga beint við csv skrárnar. Þær aðgerðir sem eru í boði eru read, write og add.

## Data

Ein csv skrá fyrir hverja gagna týpu sem er notuð í kerfinu.

## Models

Hver gagnatýpa er með sinn model klasa. Helstu aðgerðir í boði í þeim eru:

`as_dict` skilar hlutnum sem dict svo hægt sé að vista hann í csv skrá.  
`get_new_fields` skilar lista af FormField sem er notað til að búa til form þar sem notandi getur sett inn upplýsingar og bætt við nýjum hlutum í kerfið.
`get_edit_fields` skilar lista af FormField sem er notað til að búa til form þar sem notandi getur breytt gildum á hlutum sem eru til í kerfinu.

Einnig eru nokkrar set aðgerðir sem eru notaðar til að vista aðra hluti í tilvikinu sem hafa tengingu við hann. Sem dæmi þá er Employee með tengingu við Location í gegnum location_id á Employee klasanum. Þegar tilvik af Employee er sótt þá er tilvik af því Location sem notandinn tilheyrir hengt á tilvikið með því að kalla í set_location.

### Form

Klasi sem heldur utan um form field sem bjóða notanda uppá að bæta við eða breyta hlutum í kerfinu. Tilvik af þessum klasa er sent í fallið `display_form` á Screen sem sér um að birta það á réttum stað í réttum litum. Hægt er að ítra yfir tilvik af Form með for lykkju sem skilar einu tilviki af form field í hvert skipti. Hægt er að senda tilvik af FormField í edit_form_field fallið á Screen til að bjóða notanda upp á að skrifa inn upplýsingar.

### Menu

Klasi sem heldur utan um key, value par og optional connection sem er notað til að geyma token ef menu er notaður til að lista upp valmöguleika sem eru í boði. Einnig er hægt að nota Menu til að stilla upp gögnum í nokkrum línum í röð sem hafa samskonar útlit. Hægt er að senda tilvik af menu í `display_menu` fallið á Screen sem sér þá um að birta það á skjánum.

### Table

Klasi sem tekur við lista af tilvikum og header dict sem segir til um hvaða eigindi út tilvikunum á að birta og hvaða texta á að nota sem haus í hverjum dálki í töflu. Hægt er að senda tilvik af table í display_table fallið á screen sem sér um að birta töfluna á skjánum. Innifalið í birtingunni er að bjóða uppá paging ef fjöldi tilvika í listanum er meiri en hámarks fjöldi lína sem á að birta. Ef paging er virkt er hægt að nota valmöguleikann N til að fletta á næstu síðu og P til að fara á fyrri síðu.
