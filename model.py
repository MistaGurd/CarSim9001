from random import randint

class Car(object):
    def __init__(self):
        self.theEngine = Engine() # Gemmer theEngine tom klassen Engine
    def updateModel(self,dt):
        self.theEngine.updateModel(dt) # Giver theEngine updateModel egenskaberne fra Engine class

class Wheel(object):
    def __init__(self):
        self.orientation = randint(0,360) # Definere hjulenes orientation som et tal mellem 0 og 360 grader

    def rotate(self,revolutions):
        self.orientation += (revolutions * 360) # Orientationer bliver gemt som antallet af omdrejninger (revolutions) ganget 360 grader (svarende til 1 omdrejning)
        self.orientation = self.orientation % 360 # Sørger for, at hjulet altid forholder sig til 360 grader

class Engine(object):
    def __init__(self):
        self.throttlePosition = 0
        self.theGearbox = Gearbox()
        self.currentRpm = 0
        self.consumptionConstant = 0.0025
        self.maxRpm = 100
        self.theTank = Tank()
    def updateModel(self,dt):
        if self.theTank.contents > 0: # Hvis tanken ikke er tom
            self.currentRpm = self.throttlePosition * self.maxRpm

            self.theTank.remove(self.currentRpm * self.consumptionConstant) # Tanken skal fjerne currentRpm * consumptionConstant

            self.theGearbox.rotate(self.currentRpm * (dt / 60)) # Her bliver currentRpm til revolutions af delta tid divideret med 60 så regner på minutter, og ikke minutter med sekunder.
                                                                # Enhederne skal passe!

        elif self.theTank.contents <= 0: # Hvis tanken er tom
            self.currentRpm = 0 # Sæt currentRpm til 0

class Gearbox(object):
    def __init__(self):
        self.currentGear = 0
        self.clutchEngaged = False
        self.gears = [0,0.8,1,1.4,2.2,3.8]
        self.wheels = {'frontLeft' : Wheel(),
                       'frontRight' : Wheel(),
                       'rearLeft' : Wheel(),
                       'rearRight' : Wheel()
                       }
    def shiftUp(self):
        if not self.clutchEngaged and self.currentGear < 5: # Hvis kobling er nede, og nuværende gear ikke er 5
            self.currentGear += 1 # Tag nuværende gear, og gear up.
    def shiftDown(self):
        if not self.clutchEngaged and self.currentGear > 0: # Hvis kobling er nede, og nuværende gear ikke er 0
            self.currentGear -= 1 # Tag nuværende gear, og gear ned
    def rotate(self,revolutions):
        if self.clutchEngaged: # Hvis koblingen er nede:
            for wheel in self.wheels.values(): # skal hvert hjul:
                wheel.rotate(revolutions * self.gears[self.currentGear]) # Rotere med revolutions (omdrejninger fra engine) * gearets
                                                                         # position i listen self.gears

class Tank(object):
    def __init__(self):
        self.capacity = 500
        self.contents = self.capacity

    def refuel(self):
        self.contents = self.capacity # Refuel fylder tanken op med variabelværdien self.capacity

    def remove(self,amount):
        self.contents -= amount # Nuværende mængde i tanken formindskes med amount
                                # som kommer fra Engines updateModel, som at være: self.currentRpm * self.consumptionConstant
        if self.contents < 0: # tjekker om tanken er tom
            self.contents = 0 # hvis ja, så skal contents, tanken, være = 0 (så dermed tom)