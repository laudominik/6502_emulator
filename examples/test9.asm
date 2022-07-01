    .org $8000
start:
    lda #55
    sta $4000
    lda #0
loop:
    clc
    rol $4000
    clc
    adc #1
    cmp #10
    bne loop

    lda $4000



continue:

    .org $FFFC
    .word start
    .word $0000
