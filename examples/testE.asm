    .org $8000
start:

    lda #44
    sec
    sbc #20




    .org $FFFC
    .word start
    .word $0000
