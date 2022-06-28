    .org $8000
start:
    lda #0

loop:

    adc #40

    jsr loop

    .org $FFFC
    .word start
    .word $0000
