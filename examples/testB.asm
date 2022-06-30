    .org $8000
start:
    lda #1
    cmp #2
    bne eq
    lda #0
    jmp end

    eq:
    lda #3

    end:

    .org $FFFC
    .word start
    .word $0000
