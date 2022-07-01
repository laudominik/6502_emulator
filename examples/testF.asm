    .org $8000
start:

    lda #22
run:
    jsr subr


    jmp end

subr:
    sta $00
    ldx #$ff
    txa
    tay
    rts

end:
    clc
    adc $00
    bcs run

    .org $FFFC
    .word start
    .word $0000
