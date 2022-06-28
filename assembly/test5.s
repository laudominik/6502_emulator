    .org $8000
start:

    lda #64

    sta $00
    rol $00
    rol $00
    rol
    php
    adc #250
    plp

    .org $FFFC
    .word start
    .word $0000
