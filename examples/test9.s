    .org $8000
start:
    lda #1
    loop:
    adc #40
    bcc loop

continue:

    .org $FFFC
    .word start
    .word $0000
