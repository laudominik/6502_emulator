; add number to lda,
; store result on two bytes
; in memory

    .org $8000
start:

    lda #$ff
    clc
    adc #5
    sta $00
    lda #0
    adc #0
    sta $01

    .org $FFFC
    .word start
    .word $0000
