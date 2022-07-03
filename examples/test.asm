    .org $8000
start:
    lda #$fc
loop:
    clc
    adc #1

    bmi loop


    .org $FFFC
    .word start
    .word $0000
