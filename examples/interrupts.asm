    .org $8000
start:

    lda #22
    brk
    nop
    txa
    tay
    sta $00

    .org $FF00
exit:
    tsx
    rti

    .org $FFFC
    .word start
    .word $FF00
