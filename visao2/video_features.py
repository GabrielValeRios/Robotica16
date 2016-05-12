import numpy as np
import cv2
from matplotlib import pyplot as plt


MIN_MATCH_COUNT = 10

img1 = cv2.imread('calculadora.png',0)          # Imagem a procurar
 



#img2 = cv2.imread('box_in_scene.png',0)

cap = cv2.VideoCapture("video_final.mp4") 

while True:

    # Initiate SIFT detector
    sift = cv2.SIFT()

    
    ret, img2 = cap.read()



    # Imagem do cenario - puxe do video para fazer isto
    #img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)


    # find the keypoints and descriptors with SIFT in each image
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    # Configura o algoritmo de casamento de features
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Tenta fazer a melhor comparacao usando o algoritmo
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)


    if len(good)>MIN_MATCH_COUNT:
        # Separa os bons matches na origem e no destino
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)


        # Tenta achar uma trasformacao composta de rotacao, translacao e escala que situe uma imagem na outra
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        # Transforma os pontos da imagem origem para onde estao na imagem destino
        dst = cv2.perspectiveTransform(pts,M)

        # Desenha as linhas
        img2b = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.CV_AA)

        print("Sucesso")

        
        

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

    cv2.imshow('frame',img2)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
