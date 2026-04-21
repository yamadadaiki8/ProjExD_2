import os
import sys
import pygame as pg
import random
import time
WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP : (0,-5),pg.K_DOWN : (0,5),pg.K_LEFT : (-5,0), pg.K_RIGHT: (5,0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外かを判定する関数
    引数：工科トンRectまたは爆弾Rect
    戻り値：縦方向、横方向判定結果 → 画面内ならTRUE外ならFALSE
    """
    yoko, tate = True , True
    if rct.left < 0 or WIDTH < rct.right:#横方向
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：画面
    戻り値：なし 
    こうかとんと爆弾の接触判定の時にゲームオーバー画面表示
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH,HEIGHT))
    go_img.set_alpha(200)
    screen.blit(go_img,[0,0])
    
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",
    True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center =WIDTH/2,HEIGHT/2
    screen.blit(txt, txt_rct)#moji


    kk_img = pg.image.load("fig\8.png")
    kk_img2= pg.image.load("fig\8.png")
    kk_rct = kk_img.get_rect()
    kk_rct2 = kk_img2.get_rect()
    kk_rct.center = WIDTH/2+200,HEIGHT/2
    kk_rct2.center = WIDTH/2-200,HEIGHT/2
    screen.blit(kk_img, kk_rct)
    screen.blit(kk_img2, kk_rct2)


    pg.display.update()
    time.sleep(5)#修正インデントを二つあける


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                 sum_mv[0] += mv[0]
                 sum_mv[1] += mv[1]

        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])


        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #yokohoukou 
            vx*=-1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct) #爆弾を表示させる
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
