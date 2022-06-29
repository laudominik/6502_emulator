    .org $8000
start:
    lda #$ff
    cmp #$ff
    clc
    adc #1

    .org $FFFC
    .word start
    .word $0000
