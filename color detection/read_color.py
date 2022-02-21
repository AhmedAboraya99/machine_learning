import cv2 as cv
import pandas as pd

img = cv.imread('photos/stickers.jpg')
clicked = False
r = g = b = x_pos = y_pos = 0

#read Csv file
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None )

#calculate minimum distance from all colors and get the most matching color
def get_color(R, G, B):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"]))+ abs(G - int(csv.loc[i, "G"]))+abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

#get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b,g,r = res_img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

def resize_image(scale_percent): # percent of original size
    global res_img
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # cv.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])
    res_img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    return res_img

cv.namedWindow('image')
cv.setMouseCallback('image',draw_function) #call draw function when mouse clicked

while True:

    resize_image(60)
    cv.imshow('image',res_img)
    if clicked:
        # cv.rectangle(image, start point, endpoint, color, thickness)
        cv.rectangle(img, (20, 20), (720, 60), (b, g, r), -1)  #-1 fills entire rectangle
        #create text string to display (color name and RGB values
        color_text = get_color(r,g,b) + 'R ='+str(r) +  ' G=' + str(g) + ' B=' + str(b)
        # cv.putText(image,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv.putText(img,color_text,(50,50),3, 0.68, (255.255,255), 1, cv.LINE_AA )

        clicked = False
        if r + g + b >= 600:
            cv.putText(img, color_text, (50, 50), 3, 0.68, (0, 0, 0), 1, cv.LINE_AA)

    delay =20
    #wait until esc key is pressed break the loop
    if cv.waitKey(delay)& 0xFF == 27:
        break

cv.destroyAllWindows()