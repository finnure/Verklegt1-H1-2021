# User Interface

Hér fyrir neðan kemur documentation fyrir ui

## Class Screen

UI klasi sem sér um öll samskipti við terminal, bæði til að birta upplýsingar
og til að taka við innslætti frá notanda.

Við ræsingu á forriti ætti að búa til tilvik af þessum klasa án sérstakra stillinga
til að forstilla terminal og setja það í rétta stærð.

Sjálfgefin stærð glugga er 42 línur og 122 dálkar. 2 línur og 2 dálkar fara
í rammann á terminal þannig að nothæft svæði fyrir forritið er línur - 2 og
dálkar - 2. Sjálfgefin stærð á forriti er því 40 línur og 120 dálkar. Í upphafi
er reynt að stækka terminal gluggann og setja hann í rétta stærð. Ef það tekst
ekki skilar forritið villu og hættir keyrslu. Þessi virkni hefur verið prófuð
í terminal forritinu í Mac og í command prompt í Windows. Ekki er tryggt að þetta
virki í öðrum forritum.

Hægt er að búa til ný tilvik af Screen fyrir minni ramma sem eru notaðir í forritinu.
Þá verður að taka fram hversu margar línur og dálka þetta tilvik á að hafa og hvar það
á að vera staðsett. Staðsetningin er skilgreind með því að gefa upp punktinn á horninu
efst til vinstri. begin_y er línan sem á að byrja í og begin_x dálkurinn. Það þarf að
skilgreina hver parent er með því að senda tilvik af þeim glugga sem nýji glugginn
á að vera hluti af.

### Aðgerðir

#### Litir

Ef stuðningur fyrir liti er til staðar eru eftirfarandi aðgerðir í boði til að
breyta litum og stíl á texta í forritinu. Ef stuðningur við liti er ekki til
staðar er sjálfgefinn litur á texta og bakgrunn notaður, hvítur texti og
svartur bakgrunnur.

`color_pair` er par af texta lit og bakgrunns lit. Áður en hægt er að
nota par þarf að byrja á því að skilgreina hvaða tvo liti viðkomandi par inniheldur.

Í terminal forritinu á Mac er hægt að skilgreina 32767 mismunandi pör og það eru
256 mismunandi litir í boði.

```python
set_color_pair(pair: int, text_color: int, background_color: int) -> None
get_color_pair(pair: int) -> int
get_style(style_list: list) -> int
get_css_class(name: str) -> int
```

Eftirfarandi stílar eru í boði

- BOLD
- UNDERLINE
- REVERSE - Lit á texta og bakgrunni víxlað
- BLINK

Eftirfarandi css klasar eru í boði

- ERROR
- FRAME_TEXT
- OPTION
- LOGO_NAME
- LOGO_TEXT
- TABLE_HEADER
- PAGE_HEADER
- DATA_KEY

Hver stíll og hvert color pair hefur tölugildi. Til að blanda saman mörgum
stílum og nota color pair líka eru tölugildin lögð saman til að fá út
eitt gildi sem hægt er að nota.

#### Inntak og úttak

Eftirfarandi aðgerðir eru í boði til að sækja inntak frá notanda og til að
prenta texta á skjáinn.

```python
set_string_termination(termination: list = None) -> None
get_character() -> str
get_string(cols: int, filter: str = printable) -> str
get_multiline_string(lines: int = 1, cols: int = 64, filter: str = printable) -> str
print(text: str, line: int = None, col: int = None, style: int = 0) -> None
```

Termination er listi af tökkum sem ljúka innslætti á streng. Hægt er að breyta
sjálfgefnum lista með því að kalla í `set_string_termination` með nýjum lista.
Sjálfgefnir takkar eru Tab, Enter, Ör upp og Ör niður.

`get_character` bíður eftir innslætti frá notanda og skilar til baka sem streng.

`get_string` safnar saman innslegnum texta og skilar sem streng.  
Cols segir til um hversu marga stafi má taka við, sjálfgefinn fjöldi er 64.
Þegar fjöldi innsleginna stafa er orðinn jafn cols þá er innslætti sjálfkrafa
hætt og strengnum skilað.
Filter er strengur með öllum leyfilegum táknum sem notandi má slá inn.
Sjálfgefinn filter eru allir prentanlegir stafir. Utils safnið geymir nokkra
tilbúna strengi sem hægt er að nota sem filter

- PRINTABLE_IS = Allir séríslenskir stafir
- PRINTABLE = Allir prentanlegir stafir
- ALL_PRINTABLE = Báðir listar fyrir ofan sameinaðir
- NUMBERS = Tölur frá 0-9

Termination listinn er notaður til að hætta innslætti (sjá Termination ofar).  
Ef notandi slær inn staf sem er ekki leyfður er hann látinn vita með því að
blikka skjámyndinni einusinni (texta og bakgrunns litum víxlað í sekúndu).

`get_multiline_string` notar `get_string` til að safna saman línum
af strengjum. Fjöldi lína er skilgreindur í line, sjálfgefinn fjöldi 1.
Cols segir til um fjölda stafa í hverri línu, sjálfgefinn fjöldi 64.
Filter er strengur með öllum leyfilegum táknum sem notandi má slá inn.
Sjá nánari upplýsingar um filter í lýsingu fyrir `get_string` hér fyrir ofan.

`print` prentar texta á skjáinn á skilgreindri staðsetningu.
Ef line og/eða col er ekki skilgreint þá er núverandi staðsetning á bendli notuð.
Sjálfgefinn stíll á textanum er hvítur texti á svörtum bakgrunni. Hægt er að
senda útreiknað gildi í style til að breyta útliti á texta. Sjá nánar í kafla um
liti fyrir ofan.

#### Aðrar aðgerðir

```python
move_cursor_by_offset(lines: int, cols: int) -> bool
move_cursor_to_coords(line: int, col: int) -> None
clear() -> None
refresh() -> None
paint_character(style: int, line: int | None = None, col: int | None = None, num: int = 1) -> None
delete_character(line: int | None = None, col: int | None = None) -> None
delete_line(line: int | None = None) -> None
flash() -> None
flush_input() -> None
create_sub_window(begin_y: int, begin_x: int) -> _CursesWindow
end() -> None
```

`move_cursor_by_offset` færir bendilinn um fjölda lína og dálka sem tilgreind eru.  
`move_cursor_to_coords` færir bendilinn í tilgreinda línu og tilgreindan dálk.  
Báðar aðgerðir athuga fyrst hvort ný staðsetning sé innan glugga. Ef ekki þá er
aðgerð ekki framkvæmd.  
`clear` hreinsar allt sem er í viðkomandi glugga. Til að klára hreinsun þarf að kalla
í `refresh` sem uppfærir gluggann með þeim upplýsingum sem er búið að setja í hann.  
`paint_character` uppfærir stíl á staf sem er nú þegar til staðar á skjánum.
Ef line og col er skilgreint þá er stafur á viðkomandi staðsetningu uppfærður.
num segir til um fjölda stafa sem á að breyta stíl á, sjálfgefið gildi 1.  
`delete_character` hreinsar út staf á uppgefinni staðsetningu. Ef line og col er
ekki skilgreint er staf eytt út sem er undir núverandi staðsetningu á bendli.  
`delete_line` eyðir út heilli línu og færir allar línur fyrir neðan upp um eina.
Ekki er hægt að framkvæma þessa aðgerð á aðal glugganum. Ef line er uppgefin
er byrjað á því að athuga hvort sú lína sé innan viðkomandi glugga. Ef hún er það
ekki er aðgerðin ekki framkvæmd.  
`flash` víxlar litum á texta og bakgrunni í sekúndu og víxlar svo aftur til baka.
Hægt er að nota þetta sem tilkynningu til notanda.  
`flush_input` tæmir input buffer frá lyklaborði. Ef notandi var búinn að ýta á
einhverja takka þegar kallað er í `get_character()` þá man tölvan eftir þeim og
notar þá. Með því að kalla í `flush_input` er þetta minni hreinsað þannig að næsti
takki sem notandinn potar í er tekinn gildur.
`create_sub_window` Býr til nýjan glugga með begin_y línur og begin_x dálka.
Þessi gluggi erfir stillingar frá parent glugga, eins og lita prófíla.
`end` sér um að taka til í terminal og skila því í rétt ástand áður en forriti
er lokað. Það verður að kalla í þetta fall við lokun á forriti.

### Notkun
