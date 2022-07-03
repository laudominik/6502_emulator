    .org $8000
start:
    ldx #10
    lda #7
loop:

    sta $4000, X
    dex
    bpl loop

    ldx #10
loop2:

loop3:
    dec $4000, X
    bne loop3
    dex
    bpl loop2

    .org $FFFC
    .word start
    .word $0000
