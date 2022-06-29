    .org $8000
start:
    ldx #$FF
    ldy #$F0

    inx
    iny

    .org $FFFC
    .word start
    .word $0000
