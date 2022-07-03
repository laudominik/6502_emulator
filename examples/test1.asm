    .org $8000
start:
    lda #10

loop:
    pha
    sec
    sbc #1
    bpl loop

    lda #$ff
    pla
    pla
    pla


    .org $FFFC
    .word start
    .word $0000
