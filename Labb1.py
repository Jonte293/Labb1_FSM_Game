import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

STATE_START = "StartState"
STATE_TEE = "TeeState"
STATE_FAIRWAY_1 = "Fairway1State"
STATE_FAIRWAY_2 = "Fairway2State"
STATE_ROUGH = "RoughState"
STATE_BUNKER = "BunkerState"
STATE_GREEN = "GreenState"
STATE_END = "EndState"



class FSMGolfBehaviour(FSMBehaviour):
    async def on_start(self):
        print("FSM Golf Behaviour starting at TEE state")

    async def on_end(self):
        print("FSM Golf Behaviour ended at END state")
        await self.agent.stop()

class StartState(State):
    async def run(self):
        print("Välkommen till Mads Golf! \n Är du redo att spela?")
        choice = input("ja/nej\n>").strip().lower()
        if choice == "ja":
            print("Härligt, då kör vi!")
            self.set_next_state(STATE_TEE)
        elif choice == "nej": 
            print("Du har missat tiden för ditt utslag, var vänlig boka ny tid.")
            self.set_next_state(STATE_END)
        else:
            print("Felaktig inmatning, var vänlig försök igen. Skriv endast 'ja/nej'.")
            self.set_next_state(STATE_START)

class TeeState(State):
    async def run(self):
        print("Dags för ditt första slag! \n Välj klubba:\n " \
        "1. Driver \n 2. Järn-7 \n 3. Putter")
        choice = input("Ange klubba: 1/2/3\n>").strip()
        if choice == "1":
            print("Bra val! Du tog dig till Fairway med bara 50 meter kvar till green!")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_2)
        elif choice == "2":
            print("Ok val. Du landar på fairway men har fortfarande en bit kvar till green.")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_1)
        elif choice == "3":
            print("Ajdå, puttern var inget bra val. Du är kvar på tee och får försöka igen.")
            self.agent.counter += 1
            self.set_next_state(STATE_TEE)
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_TEE)

class Fairway1State(State):
    async def run(self):
        print("Du har 200 meter kvar till green, vilken klubba väljer du? \n" \
        "1. Järn 5 \n 2. Järn 7 \n 3. Putter")
        choice = input("Ange klubba: 1/2/3\n>").strip()
        if choice == "1":
            print("Bra val! Du tog dig nära green, men tyvärr landade du i en bunker..")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        elif choice == "2":
            print("Du är kvar på fairway, men bara 50 meter kvar till green!")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_2)
        elif choice == "3":
            print("Puttern var ett dåligt val, du är kvar på samma position.")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_1)
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_FAIRWAY_1)

class Fairway2State(State):
    async def run(self):
        print("Du har bara 50 meter kvar till green! Vilken klubba väljer du? \n" \
        "1. Järn 5 \n 2. Putter \n 3. Pitch \n 4. Sand wedge")
        choice = input("Ange klubba: 1/2/3/4\n>").strip()
        if choice == "1":
            print("Ajdå! Du slog alldeles för långt och hamnade i roughen..")
            self.agent.counter += 1
            self.set_next_state(STATE_ROUGH)
        elif choice == "2":
            print("Puttern var ett dåligt val, du är kvar på samma position.")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_2)
        elif choice == "3":
            print("Bra val! Du landar på green nära flagg!")
            self.agent.counter += 1
            self.set_next_state(STATE_GREEN)
        elif choice == "4":
            print("Du tar dig framåt, men landar tyvärr i bunkern precis innan green.")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_FAIRWAY_2)

class RoughState(State):
    async def run(self):
        print("Du har landat i roughen och har ingen möjlighet att spela dig upp på green.\n" \
        "Du vill spela fram dig och landa på fairway nära green. Du har 120m kvar till flagg.\n" \
        "Vilken klubba väljer du?\n" \
        "1. Järn 7 \n 2. Pitch \n 3. Putter")
        choice = input("Ange klubba: 1/2/3\n>").strip()
        if choice == "1":
            print("Bra val! Men du slog lite långt och hamnade i bunkern.")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        elif choice == "2":
            print("Snyggt! Du slog fram dig bra och landade på fairway med bara 50 meter kvar till green.")
            self.agent.counter += 1
            self.set_next_state(STATE_FAIRWAY_2)
        elif choice == "3":
            print("Tyvärr kom du ingenstans, du är kvar i roughen..")
            self.agent.counter += 1
            self.set_next_state(STATE_ROUGH)
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_ROUGH)

class BunkerState(State):
    async def run(self):
        print("Du har landat i bunkern, men nära green! Gör du ett bra slag är du uppe på green. \n" \
        "Bunkern är svårspelad, vilken klubba väljer du?\n" \
        "1. Järn 7 \n 2. Sandwedge \n 3. Hybrid 3 \n 4. putter")
        choice = input("Ange klubba: 1/2/3/4\n>").strip()
        if choice == "1":
            print("Du slår i kanten och bollen rullar tillbaks ner i bunkern..")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        elif choice == "2":
            print("Bra val! Du gör ett snyggt slag upp på green och bollen stannar nära flagg!")
            self.agent.counter += 1
            self.set_next_state(STATE_GREEN)
        elif choice == "3":
            print("Du slår i kanten och bollen rullar tillbaks ner i bunkern..")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        elif choice == "4":
            print("Bollen rullar knappt en centimeter, du bör nog välja en annan klubba..")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_BUNKER)

class GreenState(State):
    async def run(self):
        print("Du är uppe på green och nära flagg! Med rätt klubba kan du sätta den..\n" \
        "Vilken klubba väljer du?\n" \
        "1. Sandwedge \n 2. Järn 7 \n 3. Putter")
        choice = input("Välj klubba: 1/2/3\n>").strip()
        if choice == "1":
            print("Den där kan du inte putta med... Bollen rullar ned i bunkern!")
            self.agent.counter += 1
            self.set_next_state(STATE_BUNKER)
        elif choice == "2":
            print("Den klubban funkar inte så bra att putta med.. " \
            "Du missar hålet, men håller dig kvar på green..")
            self.agent.counter += 1
            self.set_next_state(STATE_GREEN)
        elif choice == "3":
            self.agent.counter += 1
            print(f"Grattis! Du satte den och är klar med denna runda. \n" \
            f"Du gick hålet på {self.agent.counter} slag.")
            if self.agent.counter == 3:
                print("Birdie!!")
            elif self.agent.counter == 4:
                print("Par!")
            elif self.agent.counter == 5:
                print("Boogey..")
            elif self.agent.counter > 5:
                print("Ställ dig på ranchen nästa gång..")
            self.set_next_state(STATE_END)

class EndState(State):
    async def run(self):
        choice = input("Vill du spela igen? 'ja/nej'\n>").strip().lower()
        if choice == "ja":
            self.agent.counter = 0
            self.set_next_state(STATE_START)
        elif choice == "nej":
            await self.agent.stop()
        else:
            print("Felaktig inmatning, försök igen.")
            self.set_next_state(STATE_END)

class Lab1_FSM_golf_Agent(Agent):
    async def setup(self):
        self.counter = 0
        fsm = FSMGolfBehaviour()
        fsm.add_state(name=STATE_START, state=StartState(), initial=True)
        fsm.add_state(name=STATE_TEE, state=TeeState())
        fsm.add_state(name=STATE_FAIRWAY_1, state=Fairway1State())
        fsm.add_state(name=STATE_FAIRWAY_2, state=Fairway2State())
        fsm.add_state(name=STATE_BUNKER, state=BunkerState())
        fsm.add_state(name=STATE_ROUGH, state=RoughState())
        fsm.add_state(name=STATE_GREEN, state=GreenState())
        fsm.add_state(name=STATE_END, state=EndState())

        fsm.add_transition(source=STATE_START, dest=STATE_TEE)
        fsm.add_transition(source=STATE_TEE, dest=STATE_FAIRWAY_1)
        fsm.add_transition(source=STATE_TEE, dest=STATE_FAIRWAY_2)
        fsm.add_transition(source=STATE_TEE, dest=STATE_TEE)
        fsm.add_transition(source=STATE_FAIRWAY_1, dest=STATE_BUNKER)
        fsm.add_transition(source=STATE_FAIRWAY_1, dest=STATE_FAIRWAY_2)
        fsm.add_transition(source=STATE_FAIRWAY_1, dest=STATE_FAIRWAY_1)
        fsm.add_transition(source=STATE_FAIRWAY_2, dest=STATE_ROUGH)
        fsm.add_transition(source=STATE_FAIRWAY_2, dest=STATE_GREEN)
        fsm.add_transition(source=STATE_FAIRWAY_2, dest=STATE_FAIRWAY_2)
        fsm.add_transition(source=STATE_FAIRWAY_2, dest=STATE_BUNKER)
        fsm.add_transition(source=STATE_ROUGH, dest=STATE_BUNKER)
        fsm.add_transition(source=STATE_ROUGH, dest=STATE_FAIRWAY_2)
        fsm.add_transition(source=STATE_ROUGH, dest=STATE_ROUGH)
        fsm.add_transition(source=STATE_BUNKER, dest=STATE_BUNKER)
        fsm.add_transition(source=STATE_BUNKER, dest=STATE_GREEN)
        fsm.add_transition(source=STATE_GREEN, dest=STATE_BUNKER)
        fsm.add_transition(source=STATE_GREEN, dest=STATE_GREEN)
        fsm.add_transition(source=STATE_GREEN, dest=STATE_END)
        fsm.add_transition(source=STATE_END, dest=STATE_START)
        self.add_behaviour(fsm)

async def main():
    fsmagent = Lab1_FSM_golf_Agent("h23jjans@yax.im", "ikb123!")
    await fsmagent.start()
    await spade.wait_until_finished(fsmagent)
    await fsmagent.stop()

if __name__ == "__main__":
    spade.run(main())
