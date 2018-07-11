;-----------------------------------------------------------------------------------------;
;					EXERCISE 2					  ;
;											  ;
;				  signed 8 bit arithmetic with carry and overflow checking;
;				  				  Created by Samuel Powell;
;						   				   4364426;
;						    				    mgu011;
;-----------------------------------------------------------------------------------------;

        	.orig   x3000

		lea	r0, start
		jmp	r0

op1     	.fill   b00001100	; must be < 256, treating as -128 to 127
op2     	.fill   b00010000	; must be < 256, treating as -128 to 127

start  		ld      r0, op1		; r0 is op1
	        ld      r1, op2		; r1 is op2
; now the arithmetic
        	add     r2, r0, r1	; r2 is cresult
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

;--------------------------;
; STUDENT CODE STARTS HERE ;
;--------------------------;
; loads up variables and output them to screen
; prints op1
		ld	r0, op1		; r0 is now op1
		jsr	printbyte	; SR 1.0
		ld	r0, newline	
		out			; write newline
; prints op2
		ld	r0, op2		; r0 is now op2
		jsr	printbyte	; SR 1.0
		ld	r0, newline
		out
; prints divider
		lea	r0, div
		puts
; prints result
		ld	r0, result	; r0 is now result
		jsr	printbyte	; SR 1.0

; prints the carry and overflow indicators
		ld	r1, carry	; r1 is now carry
		lea	r2, strcarry	; r2 is now strcarry
		jsr	postprinter	; SR 1.2

		ld	r1, overflow
		lea	r2, stroverflow
		jsr	postprinter	; SR 1.2

	        halt

;--------------------------;
;	1. SUBROUTINES	   ;
;--------------------------;
;---------------------1.0 printbyte(r0)-----------------------
; prints an 8 bit binary number(r0)
printbyte
		st	r7, reg7	; storing registers
		
		ld 	r3, counter
		lea	r2, sign8
nextmask	ldr	r1, r2, #0
		jsr	printcurrent	; SR 1.1
		add	r2, r2, #1
		add	r3, r3, #-1
		brp	nextmask
		ld	r0, space
		out

		ld	r7, reg7	; loading registers
		RET

;---------------------1.1 printcurrent(r0, r1)----------------
; prints the digit(r0) at the current index(r1)
printcurrent
		st	r7, reg2_7	; storing registers
		st	r0, reg2_0
		st	r1, reg2_1

		and	r0, r0, r1	; is a non zero digit produced
		brz	print0
		ld	r0, one
		out			; print a "1" to screen
		brnzp 	printrestore
print0		ld	r0, zero	
		out			; print a "0" to screen

printrestore	ld	r7, reg2_7	; loading registers
		ld	r0, reg2_0
		ld	r1, reg2_1
		RET

;---------------------1.2 postprinter(r1, r2)-----------------
; looks at information(r1) and prints a symbol(r2)
postprinter
		st	r7, reg7	; storinging registers
		st	r1, reg1

		add	r1, r1, #-1	; r1 is no longer r1
		brz	printsymbol
		ld	r0, space
		out
		out			; carry or overflow not set
		brnzp	postprintfinal	
printsymbol	and	r0, r0, #0
		add	r0, r2, #0	; r2 is now r0
		puts			; print r2 (c or v)
postprintfinal	
		ld	r7, reg7	; loading registers
		ld	r1, reg1
		RET	

;--------------------------;
;	Variables	   ;
;--------------------------;
mask		.fill	b11111111
signbit		.fill	b10000000
carrybit	.fill	b100000000
counter		.fill	b00001000	;how many characters to print (8)
result  	.blkw   1
carry   	.blkw   1
overflow    	.blkw   1

; masks used to check certain positions
sign8		.fill	b10000000
sign7		.fill	b01000000
sign6		.fill	b00100000
sign5		.fill	b00010000
sign4		.fill	b00001000
sign3		.fill	b00000100
sign2		.fill	b00000010
sign1		.fill	b00000001

; strings for printing
one		.stringz	"1"
zero		.stringz	"0"
div		.stringz	"========\n"
newline		.stringz	"\n"
space		.stringz	" "
strcarry	.stringz	"c "
stroverflow	.stringz	"v "

; registry storing/loading
reg0		.blkw	1
reg1		.blkw	1
reg2		.blkw	1
reg7		.blkw	1
;primitive stack (don't judge me!)
reg2_0		.blkw	1
reg2_1		.blkw	1
reg2_7		.blkw	1



		.end