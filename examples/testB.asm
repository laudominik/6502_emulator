    .org $8000
start:
    lda #1
    eor #3
    brk
    nop

    .org $FF00
halt:
    jmp halt

    .org $FFFC
    .word start
    .word $FF00
