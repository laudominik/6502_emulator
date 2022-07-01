    .org $8000
start:

    ldy #1
    dey
    dey
    dey

    .org $FFFC
    .word start
    .word $0000
