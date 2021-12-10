Report/ inniheldur skýrsluna og öll hönnunarskjöl
Code/ inniheldur allan kóðann.
Code/main.py er aðal forritið
Keyrið forritið með því að fara inn í Code möppuna og keyra
python main.py
eða
python3 main.py

Kröfur:
Mac þarf að keyra forritið í terminal (ekki iTerm, innbyggðu vscode terminal eða öðru)
Engir auka pakkar í Mac
Prófað á útgáfu 3.8.9, ætti að virka á 3.9.x

Windows þarf að keyra forritið í command prompt, ekki prófað í powershell.
Það þarf að setja upp windows-curses
pip install windows-curses
Prófað á útgáfu 3.9.x

Ekki prófað á linux

Notendur:
Eingöngu þarf að stimpla inn 3ja stafa id til að skrá sig inn í kerfið.

Manager ids = 100, 103, 106
Employee ids = Öll önnur id frá 101 upp í 114

Nokkur atriði sem gott er að hafa í huga við notkun kerfisins:

•	Ekki er hægt að bakka til baka úr add og edit formum, klára verður innsláttinn og hætta svo við breytingarnar
•	Öll leit eftir auðkennum miðast við kerfisauðkenni sem er 3 stafa tala. Það er ljóst að það þarf mjög fljótlega 
    að stækka þetta auðkenni upp í a.m.k. fjóra stafi
•	Í núverandi mynd býður kerfið eingöngu upp á að stofna stafsmann en ekki yfirmenn styður ekki breytingar
     á hlutverkum starfsmanna. Úr þessu verður bætt fjótlega. 
•	Tekin var ákvörðun um að eingöngu væri hægt að stofna verkbeiðnar út frá fasteignum, þannig veit kerfið 
    alltaf hvaða auðkennisnúmer á að fylgja verkbeiðni. 
•	Þegar niðurstöður síunnar eru birtar koma þær í lista þó með þeirri undantekningu að þegar aðeins 
    eitt atriði uppfyllir síunarkröfur opnast það atriði beint en birtist ekki í lista. 


Hlekkur á myndband:

