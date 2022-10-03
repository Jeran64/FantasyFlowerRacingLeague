from PIL import Image, ImageDraw, ImageFilter
import random
distance=100
contestants=50 #feasable max of 256 for now
flowerGrowRate=.5;
contestRound=0;

canvas=Image.new("RGBA",(distance,contestants),0) #create our racing lanes. There will be one contestant per lane.
nextFrame=canvas;#create a duplicate. we will save the data here.
playArea=ImageDraw.Draw(nextFrame)

pixels=canvas.load()

flowersWithNeighbors=[]

colorList=[];

#load the left side with different colors. pick colors via a chunky gradient along the hue axis in the HSL space.
#store list of pixels with full opacity in AdultFlowers
#use neighbor finding algorithm on AdultFlowers, to make a list of transparent neighbors to AdultFlowers.
#decide where new flowers grow
#Cull AdultFlowers list of those that have 8 neighbors (child or adult flowers)

directions=[(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]


def initializeContenders(contestantCount):
    for a in range(0,contestantCount-1):
        randomColor=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)) #pick a random color because im frustrated at using HSV values to do it.
        colorList.append(randomColor);
        playArea.point((0,a),randomColor);
        flowersWithNeighbors.append((0,a)); #save the coordinates of our pixels.

    canvas.save("temps.png")
    

def runContest():
    global contestRound, canvas, nextFrame; #global variable are cool
    contestRound=contestRound+1;
    pixels=canvas.load()#refresh our list of pixels. 
    for x in range(0,distance):
        for y in range(0,contestants):
            if(pixels[x,y][3]==0): #if the 4th value (alpha) is transparent
                potentialParents=[];#clear a list for our potental parents.
                for offset in directions: #check all the locations around us
                    cheeckingCoords=(x+offset[0],y+offset[1])#save our offset coordinates
                    if(cheeckingCoords[0]>=distance or cheeckingCoords[0]<0 or cheeckingCoords[1]>=contestants or cheeckingCoords[1]<0):
                        pass; 
                    elif(pixels[cheeckingCoords][3]==255):##if the opacity of the pixel is opaque, it means it is an adult, and can be used.
                        #print("found a neighbor at");
                        #print(cheeckingCoords);
                        potentialParents.append(pixels[cheeckingCoords]) #and then add it to the list.
                #decide if a flower is growing there or not.
                if(potentialParents and random.random()<=flowerGrowRate):
                    #if we are here, we have decided to grow. Use the list of potential parents to pick one.
                    random.shuffle(potentialParents);#randomize.
                    newFlower=potentialParents[0];
                    playArea.point((x,y),(newFlower[0],newFlower[1],newFlower[2],64));#plant the new flower! plant it at 64 transparency. this represents a bud.
            elif(pixels[x,y][3]==128):
                newFlower=pixels[x,y];
                playArea.point((x,y),(newFlower[0],newFlower[1],newFlower[2],255));
                
            elif(pixels[x,y][3]==64):
                newFlower=pixels[x,y];
                playArea.point((x,y),(newFlower[0],newFlower[1],newFlower[2],128));
            
    canvas=nextFrame;
    canvas.save(str(contestRound)+"FRL.png");#save the results.
    

def checkWinner():
    for a in range(0,contestants):
        if(pixels[distance-2,a][3]==255):#check to see aif theres any opaque pixels ont he final column of pixels.
            return True
    return False;

initializeContenders(contestants);#draw a line of contestants on the left.
while (checkWinner()==False):
    runContest();
    print(contestRound);
