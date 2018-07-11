;-----------------------------------------------------------------------------------------;
;					EXERCISE 3					  ;
;											  ;
;				 signed 30 bit arithmetic with carry and overflow checking;
;				  				  Created by Samuel Powell;
;						   				   4364426;
;						    				    mgu011;
;-----------------------------------------------------------------------------------------;

        	.orig   x3000

		lea	r0, start
		jmp	r0

op1_lsw     	.fill   b100000000000001
op1_msw     	.fill   b100000000000001; must be <1,073,741,824, treating as -536,870,912 to 536,870,911
op2_lsw     	.fill   b100000000000001
op2_msw     	.fill   b100000000000000; must be <1,073,741,824, treating as -536,870,912 to 536,870,911

; add op1_lsw(r0), op2_lsw(r1). Set result_lsw, carry_lsw	
start		ld      r0, op1_lsw	; r0 is op1
	        ld      r1, op2_lsw	; r1 is op2
		jsr	add15		; SR 1.0
		jsr	lsw_post	; SR 1.1
; add op1_msw(r0), op2_msw(r1). If carry_lsw exists, add one to result, Set result(msw)
		ld      r0, op1_msw	; r0 is op1
	        ld      r1, op2_msw	; r1 is op2
		jsr	add15		; SR 1.0
		jsr	msw_post	; SR 1.2
; prints op1
		ld	r0, op1_msw
		ld	r1, op1_lsw
		jsr 	print30		; SR 1.3
		ld	r0, newline
		out
; prints op2
		ld	r0, op2_msw
		ld	r1, op2_lsw
		jsr 	print30		; SR 1.3
		ld	r0, newline
		out
; prints divider
		lea	r0, div
		puts
; prints result
		ld	r0, result
		ld	r1, result_lsw
		jsr 	print30		; SR 1.3
; prints carry
		ld	r1, carry	
		lea	r2, strcarry
		jsr	postprinter	; SR 1.6
; prints overflow
		ld	r1, overflow
		lea	r2, stroverflow
		jsr	postprinter	; SR 1.6
	        halt

;--------------------------;
;	1. SUBROUTINES	   ;
;--------------------------;
;--------------------------1.0 add15(r0, r1)-------------------------------------------------
; takes two 15 bit numbers (r0, r1) and adds them while setting carry and overflow
add15		add     r2, r0, r1	; r2 is cresult
		ld	r3, mask
		and	r3, r2, r3	; r3 is result
        	st      r3, result
; carry
		and	r3, r3, #0	; clear r3, carry
		ld	r4, carrybit	; r4 is carrybit
        	and     r4, r2, r4
		brz	nocarry
		add	r3, r3, #1
nocarry        	st      r3, carry
; overflow
		and	r3, r3, #0
		ld	r4, signbit	; r4 is signbit
		and	r0, r0, r4	; r0 no longer op1
		brz	plus1
		add	r3, r3, #1
plus1		add	r0, r3, #0	; r0 sign1
		and	r3, r3, #0
		and	r1, r1, r4	; r1 no longer op1
		brz	plus2
		add	r3, r3, #1
plus2		add	r1, r3, #0	; r1 sign2
		and	r3, r3, #0
		and	r2, r2, r4	; r2 no longer cresult
		brz	plus3
		add	r3, r3, #1
plus3		add	r2, r3, #0	; r2 is signres
		and	r3, r3, #0
; we need to compare sign1(r0) with sign2(r1)
		not	r0, r0
		add	r0, r0, #1	; 2's complement
		add	r1, r1, r0	; subtraction
		brnp	different
; compare signres(r2) with sign1(r0)
		add	r2, r2, r0	; subtraction
		brz	different	; actually the same
		add	r3, r3, #1
different	st	r3, overflow
		RET
;--------------------------1.1 lsw_post()---------------------------------------------------
; sets result_lsw and carry_lsw
lsw_post	
		ld	r0, result
		st	r0, result_lsw
		ld	r0, carry
		st	r0, carry_lsw
		RET
;--------------------------1.2 msw_post()---------------------------------------------------
; checks if carry_lsw exists, and increments result by one if it does
msw_post	
		ld	r0, carry_lsw
		ld	r1, result
		add	r0, r0, #-1	; r0 is no longer carry_lsw
		brnp	noadd
		add	r1, r1, #1
noadd		st	r1, result
		RET
;--------------------------1.3 print30(r0, r1)----------------------------------------------
; prints the two parts that make up our 30 bit number. MSW(r0) and LSW(r4)
print30
		st	r7, reg3_7	; storing registers

		jsr	print15 	; SR 1.4
		and	r0, r0, #0
		add	r0, r0, r1	; r1 is now r0
		jsr	print15 	; SR 1.4

		ld	r7, reg3_7	; restoring registers
		RET
;--------------------------1.4 print15(r0)--------------------------------------------------
; prints a 15 bit number(r0)
print15
		st	r7, reg7	; storing registers
		st	r1, reg1

		ld	r3, counter	; loop control
		lea	r2, sign15	; r2 is current mask address
nextmask	ldr	r1, r2, #0	; r1 is current mask value
		jsr	printcurrent	; SR 1.5
		add	r2, r2, #1
		add	r3, r3, #-1
		brp	nextmask

		ld	r0, space
		out

		ld	r7, reg7	; restoring registers
		ld	r1, reg1
		RET
;--------------------------1.5 printcurrent(r0, r1)-----------------------------------------
; prints the digit(r0) at the current index(r1)
printcurrent
		st	r7, reg2_7	; storing registers
		st	r0, reg2_0

		and	r0, r0, r1	; r0 is not r0
		brz	print0
		ld	r0, one
		out			; print a "1" to screen
		brnzp 	printrestore
print0		ld	r0, zero	
		out			; print a "0" to screen

printrestore	ld	r7, reg2_7	; restoring registers	
		ld	r0, reg2_0
		RET

;--------------------------1.6 postprinter(r1, r2)------------------------------------------
; loads a variable(r1) to check and prints a str(r2)
postprinter
		st	r7, reg7	; storing registers

		add	r1, r1, #-1	; r1 is not r1
		brz	printsymbol
		ld	r0, space
		out
		out			; carry or overflow not set
		brnzp	postprintfinal	
printsymbol	and	r0, r0, #0
		add	r0, r2, #0	; r2 is now r0
		puts
postprintfinal
		ld	r7, reg7	; restoring registers
		RET	

;--------------------------;
;	2. Variables	   ;
;--------------------------;
mask		.fill	b111111111111111
signbit		.fill	b100000000000000
carrybit	.fill	b1000000000000000
counter		.fill	b1111
result		.blkw	1
result_lsw  	.blkw   1
carry   	.blkw   1
carry_lsw   	.blkw   1
overflow    	.blkw   1

; masks used to check certain indices
sign15		.fill	b0100000000000000
sign14		.fill	b0010000000000000
sign13		.fill	b0001000000000000
sign12		.fill	b0000100000000000
sign11		.fill	b0000010000000000
sign10		.fill	b0000001000000000
sign9		.fill	b0000000100000000
sign8		.fill	b0000000010000000
sign7		.fill	b0000000001000000
sign6		.fill	b0000000000100000
sign5		.fill	b0000000000010000
sign4		.fill	b0000000000001000
sign3		.fill	b0000000000000100
sign2		.fill	b0000000000000010
sign1		.fill	b0000000000000001

; strings for printing
one		.stringz	"1"
zero		.stringz	"0"
div		.stringz	"=============== ===============\n"
newline		.stringz	"\n"
space		.stringz	" "
strcarry	.stringz	"c "
stroverflow	.stringz	"v "

; registry storing/loading
reg0		.blkw	1
reg1		.blkw	1
reg2		.blkw	1
reg7		.blkw	1
; primitive stack for second tier subroutine calls(don't judge me!)
reg2_0		.blkw	1
reg2_7		.blkw	1
reg3_7		.blkw	1

		.end