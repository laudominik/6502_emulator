    .org $8000
start:
    lda #2

    ror
    bcc even
    clc
    adc #1

    even:




    .org $FFFC
    .word start
    .word $0000
