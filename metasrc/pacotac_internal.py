from __future__ import print_function
import sys
from pacolib import *

if len(sys.argv) < 2:
    sys.stderr.write('\nUsage: '+sys.argv[0]+' relsize\n\n')
    sys.exit(1)

relsize = int(sys.argv[1])

print ('From Paco Require Export paconotation_internal paconotation.')
print ('Set Implicit Arguments.')
print ()
print ('(** * Tactic support for [paco] library')
print ()
print ('    This file defines tactics for converting the conclusion to the right form so')
print ('    that the accumulation lemmas can be usefully applied. These tactics are used')
print ('    in both internal and external approaches.')
print ()
print ('    Our main tactic, [pcofix], is defined at the end of the file and')
print ('    works for predicates of arity up to 14.')
print ('*)')
print ()
print ('(** ** Internal tactics *)')
print ()
print ('Ltac get_concl := lazymatch goal with [ |- ?G ] => G end.')
print ()
print ('Inductive _paco_mark := _paco_mark_cons.')
print ()
print ('Inductive _paco_foo := _paco_foo_cons.')
print ()
print ('Definition _paco_id {A} (a : A) : A := a.')
print ()
print ('Inductive paco_ex (A : Type) (P : A -> Prop) : Prop :=')
print ('| paco_ex_intro : forall x : A, P x -> @paco_ex A P.')
print ()
print ('Inductive paco_and (A B : Prop) : Prop :=')
print ('| paco_conj : A -> B -> @paco_and A B.')
print ()
print ('Ltac paco_generalize_hyp mark :=')
print ('  let y := fresh "_paco_rel_" in')
print ('  match goal with')
print ('  | [x: ?A |- _] =>')
print ('    match A with')
print ('    | mark => clear x')
print ('    | _ => intro y;')
print ('      match type of y with')
print ('        | context[x] => revert x y;')
print ('          match goal with [|-forall x, @?f x -> _] =>')
print ('            intros x y; generalize (@paco_ex_intro _ f x y)')
print ('          end')
print ('        | _ => generalize (@paco_conj _ _ (@paco_ex_intro _ _ x _paco_foo_cons) y)')
print ('      end; clear x y; paco_generalize_hyp mark')
print ('    end')
print ('  end.')
print ()
print ('Ltac paco_destruct_hyp mark :=')
print ('  match goal with')
print ('  | [x: ?A |- _] =>')
print ('    match A with')
print ('    | mark => idtac')
print ('    | _paco_foo => clear x; paco_destruct_hyp mark')
print ("    | @paco_ex _ (fun n => _) => let n' := fresh n in destruct x as (n', x); paco_destruct_hyp mark")
print ("    | @paco_and _ _ => let x' := fresh x in destruct x as (x,x'); paco_destruct_hyp mark")
print ('    end')
print ('  end.')
print ()
print ('Ltac paco_revert_hyp mark :=')
print ('  match goal with [x: ?A |- _] =>')
print ('  match A with')
print ('    | mark => clear x')
print ('    | _ => revert x; paco_revert_hyp mark')
print ('  end end.')
print ()
print ('Ltac paco_post_var INC pr cr := let TMP := fresh "_paco_tmp_" in')
print ('  repeat (')
print ('    match goal with [H: context f [pr] |-_] =>')
print ('      let cih := context f [cr] in rename H into TMP;')
print ('      assert(H : cih) by (repeat intro; eapply INC, TMP; eassumption); clear TMP')
print ('    end);')
print ('  clear INC pr.')
print ()
print ('Ltac paco_rename_last :=')
print ('  let x := fresh "_paco_xxx_" in match goal with [H: _|-_] => rename H into x end.')
print ()
print ('Ltac paco_simp_hyp CIH :=')
print ('  let EP := fresh "_paco_EP_" in')
print ('  let FP := fresh "_paco_FF_" in')
print ('  let TP := fresh "_paco_TP_" in')
print ('  let XP := fresh "_paco_XP_" in')
print ('  let PP := type of CIH in')
print ('  evar (EP: Prop);')
print ('  assert (TP: False -> PP) by (')
print ('    intros FP; generalize _paco_mark_cons;')
print ('    repeat intro; paco_rename_last; paco_destruct_hyp _paco_mark;')
print ('    paco_revert_hyp _paco_mark;')
print ('    let con := get_concl in set (TP:=con); revert EP; instantiate (1:= con); destruct FP);')
print ('  clear TP;')
print ('  assert (XP: EP)')
print ('    by (unfold EP; clear -CIH; generalize _paco_mark_cons; repeat intro; apply CIH; paco_revert_hyp _paco_mark;')
print ('        repeat (let x := fresh "x" in intro x; generalize _paco_mark_cons; intros;')
print ('                first [exists x|split; [exists x; apply _paco_foo_cons|]];')
print ('                paco_revert_hyp _paco_mark);')
print ('        unfold _paco_id; reflexivity);')
print ('  unfold EP in *; clear EP CIH; rename XP into CIH.')
print ()
print ('Ltac paco_post_simp CIH :=')
print ('  let CIH := fresh CIH in')
print ('  intro CIH; paco_simp_hyp CIH;')
print ('  first [try(match goal with [ |- context[_paco_id] ] => fail 2 | [ |- context[_paco_foo] ] => fail 2 end) |')
print ('    let TMP := fresh "_paco_TMP_" in')
print ('    generalize _paco_mark_cons; intro TMP;')
print ('    repeat intro; paco_rename_last; paco_destruct_hyp _paco_mark;')
print ('    paco_revert_hyp _paco_mark')
print ('  ].')
print ()
print ('Ltac paco_ren_r nr cr :=')
print ('  first [rename cr into nr | let nr := fresh nr in rename cr into nr].')
print ()
print ('Ltac paco_ren_pr pr cr := rename cr into pr.')
print ()
print ('Ltac paco_revert :=')
print ('  match goal with [H: _ |- _] => revert H end.')
print ('')


for n in range (0,relsize+1):
    print ("Section SIG"+str(n)+".")
    print ("")
    for i in range(n):
        print ("Variable T"+str(i)+" : "+ifpstr(i,"forall"),end="")
        for j in range(i):
            print (" (x"+str(j)+": @T"+str(j)+itrstr(" x",j)+")",end="")
        print (ifpstr(i,", ")+"Type.")
    print ("")
    print ("(** ** Signatures *)")
    print ("")
    print ("Record sig"+str(n)+"T  :=")
    print ("  exist"+str(n)+"T {")
    for i in range(n):
        print ("      proj"+str(n)+"T"+str(i)+": @T"+str(i)+itrstr(" proj"+str(n)+"T", i)+";")

    print ("    }.")
    print ("Definition uncurry"+str(n)+"  (R: rel"+str(n)+""+itrstr(" T", n)+"): rel1 sig"+str(n)+"T :=")
    print ("  fun x => R"+itrstr(" (proj"+str(n)+"T", n, " x)")+".")
    print ("Definition curry"+str(n)+"  (R: rel1 sig"+str(n)+"T): rel"+str(n)+""+itrstr(" T", n)+" :=")
    print ("  "+ifpstr(n, "fun"+itrstr(" x", n)+" =>")+" R (@exist"+str(n)+"T"+itrstr(" x", n)+").")
    print ("")
    print ("Lemma uncurry_map"+str(n)+" r0 r1 (LE : r0 <"+str(n)+"== r1) : uncurry"+str(n)+" r0 <1== uncurry"+str(n)+" r1.")
    print ("Proof. intros [] H. apply LE. apply H. Qed.")
    print ("")
    print ("Lemma uncurry_map_rev"+str(n)+" r0 r1 (LE: uncurry"+str(n)+" r0 <1== uncurry"+str(n)+" r1) : r0 <"+str(n)+"== r1.")
    print ("Proof.")
    print ("  red; intros. apply (LE (@exist"+str(n)+"T"+itrstr(" x", n)+") PR).")
    print ("Qed.")
    print ("")
    print ("Lemma curry_map"+str(n)+" r0 r1 (LE: r0 <1== r1) : curry"+str(n)+" r0 <"+str(n)+"== curry"+str(n)+" r1.")
    print ("Proof. ")
    print ("  red; intros. apply (LE (@exist"+str(n)+"T"+itrstr(" x", n)+") PR).")
    print ("Qed.")
    print ("")
    print ("Lemma curry_map_rev"+str(n)+" r0 r1 (LE: curry"+str(n)+" r0 <"+str(n)+"== curry"+str(n)+" r1) : r0 <1== r1.")
    print ("Proof. ")
    print ("  intros [] H. apply LE. apply H.")
    print ("Qed.")
    print ("")
    print ("Lemma uncurry_bij1_"+str(n)+" r : curry"+str(n)+" (uncurry"+str(n)+" r) <"+str(n)+"== r.")
    print ("Proof. unfold le"+str(n)+". intros. apply PR. Qed.")
    print ("")
    print ("Lemma uncurry_bij2_"+str(n)+" r : r <"+str(n)+"== curry"+str(n)+" (uncurry"+str(n)+" r).")
    print ("Proof. unfold le"+str(n)+". intros. apply PR. Qed.")
    print ("")
    print ("Lemma curry_bij1_"+str(n)+" r : uncurry"+str(n)+" (curry"+str(n)+" r) <1== r.")
    print ("Proof. intros [] H. apply H. Qed.")
    print ("")
    print ("Lemma curry_bij2_"+str(n)+" r : r <1== uncurry"+str(n)+" (curry"+str(n)+" r).")
    print ("Proof. intros [] H. apply H. Qed.")
    print ("")
    print ("Lemma uncurry_adjoint1_"+str(n)+" r0 r1 (LE: uncurry"+str(n)+" r0 <1== r1) : r0 <"+str(n)+"== curry"+str(n)+" r1.")
    print ("Proof.")
    print ("  apply uncurry_map_rev"+str(n)+". eapply le1_trans; [apply LE|]. apply curry_bij2_"+str(n)+".")
    print ("Qed.")
    print ("")
    print ("Lemma uncurry_adjoint2_"+str(n)+" r0 r1 (LE: r0 <"+str(n)+"== curry"+str(n)+" r1) : uncurry"+str(n)+" r0 <1== r1.")
    print ("Proof.")
    print ("  apply curry_map_rev"+str(n)+". eapply le"+str(n)+"_trans; [|apply LE]. apply uncurry_bij2_"+str(n)+".")
    print ("Qed.")
    print ("")
    print ("Lemma curry_adjoint1_"+str(n)+" r0 r1 (LE: curry"+str(n)+" r0 <"+str(n)+"== r1) : r0 <1== uncurry"+str(n)+" r1.")
    print ("Proof.")
    print ("  apply curry_map_rev"+str(n)+". eapply le"+str(n)+"_trans; [apply LE|]. apply uncurry_bij2_"+str(n)+".")
    print ("Qed.")
    print ("")
    print ("Lemma curry_adjoint2_"+str(n)+" r0 r1 (LE: r0 <1== uncurry"+str(n)+" r1) : curry"+str(n)+" r0 <"+str(n)+"== r1.")
    print ("Proof.")
    print ("  apply uncurry_map_rev"+str(n)+". eapply le1_trans; [|apply LE]. apply curry_bij1_"+str(n)+".")
    print ("Qed.")
    print ("")
    print ("End SIG"+str(n)+".")

print ('(** *** Arity 0')
print ('*)')
print ()
print ('Ltac paco_cont0 :=')
print ('generalize _paco_foo_cons; paco_generalize_hyp _paco_mark.')
print ()
print ('Ltac paco_pre0 :=')
print ('generalize _paco_mark_cons; repeat intro; paco_cont0.')
print ()
print ('Ltac paco_post_match0 INC tac1 tac2 :=')
print ('let cr := fresh "_paco_cr_" in intros cr INC; repeat (red in INC);')
print ('match goal with [H: ?x |- _] => match x with')
print ('| bot0 -> _ => clear H; tac1 cr')
print ('| ?pr -> _ => paco_post_var INC pr cr; tac2 pr cr')
print ('| _ => tac1 cr')
print ('end end.')
print ()
print ('Tactic Notation "paco_post0" ident(CIH) "with" ident(nr) :=')
print ('let INC := fresh "_paco_inc_" in')
print ('paco_post_match0 INC ltac:(paco_ren_r nr) paco_ren_pr; paco_post_simp CIH;')
print ("let CIH' := fresh CIH in try rename INC into CIH'.")
print ()

for n in range (1,relsize+1):
    print ("(** *** Arity "+str(n))
    print ("*)")
    print ()

    print ('Lemma _paco_convert'+str(n)+': forall'+itrstr(' T',n))
    print ('(paco'+str(n)+': forall')
    for i in range(n):
        print ('(y'+str(i)+': @T'+str(i)+itrstr(' y', i)+')')
    print (', Prop)')
    print (itrstr(' y', n))
    print ('(CONVERT: forall')
    for i in range(n):
        print ('(x'+str(i)+': @T'+str(i)+itrstr(' x', i)+')')
    print ('(EQ: _paco_id (@exist'+str(n)+'T'+itrstr(' T', n)+itrstr(' x', n)+' = @exist'+str(n)+'T'+itrstr(' T', n)+itrstr(' y', n)+'))')
    print (', @paco'+str(n)+itrstr(' x', n)+'),')
    print ('@paco'+str(n)+itrstr(' y', n)+'.')
    print ('Proof. intros. apply CONVERT; reflexivity. Qed.')
    print ()

    print ('Lemma _paco_convert_rev'+str(n)+': forall'+itrstr(' T',n))
    print ('(paco'+str(n)+': forall')
    for i in range(n):
        print ('(y'+str(i)+': @T'+str(i)+itrstr(' y', i)+')')
    print (', Prop)')
    print (itrstr(' y', n))
    print (itrstr(' x', n))
    print ('(EQ: _paco_id (@exist'+str(n)+'T'+itrstr(' T', n)+itrstr(' x', n)+' = @exist'+str(n)+'T'+itrstr(' T', n)+itrstr(' y', n)+'))')
    print ('(PACO: @paco'+str(n)+itrstr(' y', n)+'),')
    print ('@paco'+str(n)+itrstr(' x', n)+'.')
    print ('Proof. intros.')
    print ('apply (@f_equal (@sig'+str(n)+'T'+itrstr(' T', n)+') _ (fun x => @paco'+str(n))
    for i in range(n):
        print (' x.(proj'+str(n)+'T'+str(i)+')')
    print (')) in EQ. simpl in EQ. rewrite EQ. apply PACO.')
    print ('Qed.')
    print ()

    print ('Ltac paco_convert_rev'+str(n)+' := match goal with')
    print ('| [H: _paco_id (@exist'+str(n)+'T'+(' _' * n)+itrstr(' ?x', n)+' = @exist'+str(n)+'T'+(' _' * n)+itrstr(' ?y', n)+') |- _] =>')
    print ('eapply _paco_convert_rev'+str(n)+'; [eapply H; clear H|..]; clear'+itrstr(' x', n)+' H')
    print ('end.')
    print ()

    print ("Ltac paco_cont"+str(n)+itrstr(" e",n)+" :=")
    for i in range(n):
        print ('let x'+str(i)+' := fresh "_paco_v_" in')
    print ('apply _paco_convert'+str(n)+';')
    print ('intros'+itrstr(' x', n)+';')
    print (itrstr('move x',n-1,' at top; ')+'move x'+str(n-1)+' at top;')
    print ('paco_generalize_hyp _paco_mark; revert'+itrstr(' x',n)+'.')
    print ()

    print ('Lemma _paco_pre'+str(n)+': forall'+itrstr(' T',n)+' (gf: rel'+str(n)+itrstr(' T',n)+')'+itrstr(' x',n))
    print ("(X: let gf' := gf in gf'"+itrstr(" x",n)+"), gf"+itrstr(" x",n)+".")
    print ('Proof. intros; apply X. Defined.')
    print ()

    print ('Ltac paco_pre'+str(n)+' := let X := fresh "_paco_X_" in')
    print ('generalize _paco_mark_cons; repeat intro;')
    print ('apply _paco_pre'+str(n)+';')
    print ('match goal with')
    print ('| [|- let _ : _'+itrstr(' ?T',n)+' := _ in _'+itrstr(' ?e',n)+'] => intro X; unfold X; clear X;')
    print ('paco_cont'+str(n))
    for i in range(n):
        print (' (e'+str(i)+': T'+str(i)+itrstr(' e',i)+')')
    print ('end.')
    print ()

    print ('Ltac paco_post_match'+str(n)+' INC tac1 tac2 :=')
    print ('let cr := fresh "_paco_cr_" in intros cr INC; repeat (red in INC);')
    print ('match goal with [H: ?x |- _] => match x with')
    print ('| forall'+n*' _'+', bot'+str(n)+n*' _'+' -> _ => clear H; tac1 cr')
    print ('| forall'+n*' _'+', ?pr'+n*' _'+' -> _ => paco_post_var INC pr cr; tac2 pr cr')
    print ('| _ => tac1 cr')
    print ('end end.')
    print ()

    print ('Ltac paco_simp_hyp'+str(n)+' CIH :=')
    print ('  let EP := fresh "_paco_EP_" in')
    print ('  let FP := fresh "_paco_FF_" in')
    print ('  let TP := fresh "_paco_TP_" in')
    print ('  let XP := fresh "_paco_XP_" in')
    print ('  let PP := type of CIH in')
    print ('  evar (EP: Prop);')
    print ('  assert (TP: False -> PP) by (')
    print ('    intros FP; generalize _paco_mark_cons;')
    print ('    repeat intro; paco_rename_last; paco_destruct_hyp _paco_mark;')
    print ('    paco_convert_rev'+str(n)+'; paco_revert_hyp _paco_mark;')
    print ('    let con := get_concl in set (TP:=con); revert EP; instantiate (1:= con); destruct FP);')
    print ('  clear TP;')
    print ('  assert (XP: EP)')
    print ('    by (unfold EP; clear -CIH; generalize _paco_mark_cons; repeat intro; apply CIH; paco_revert_hyp _paco_mark;')
    print ('        repeat (let x := fresh "x" in intro x; generalize _paco_mark_cons; intros;')
    print ('                first [exists x|split; [exists x; apply _paco_foo_cons|]];')
    print ('                paco_revert_hyp _paco_mark);')
    print ('        unfold _paco_id; reflexivity);')
    print ('  unfold EP in *; clear EP CIH; rename XP into CIH.')
    print ()
    print ('Ltac paco_post_simp'+str(n)+' CIH :=')
    print ('  let CIH := fresh CIH in')
    print ('  intro CIH; paco_simp_hyp'+str(n)+' CIH;')
    print ('  first [try(match goal with [ |- context[_paco_id] ] => fail 2 | [ |- context[_paco_foo] ] => fail 2 end) |')
    print ('    let TMP := fresh "_paco_TMP_" in')
    print ('    generalize _paco_mark_cons; intro TMP;')
    print ('    repeat intro; paco_rename_last; paco_destruct_hyp _paco_mark;')
    print ('    paco_convert_rev'+str(n)+'; paco_revert_hyp _paco_mark')
    print ('  ].')
    print ()

    print ('Tactic Notation "paco_post'+str(n)+'" ident(CIH) "with" ident(nr) :=')
    print ('let INC := fresh "_paco_inc_" in')
    print ('paco_post_match'+str(n)+' INC ltac:(paco_ren_r nr) paco_ren_pr; paco_post_simp'+str(n)+' CIH;')
    print ("let CIH' := fresh CIH in try rename INC into CIH'.")
    print ()

print ("(** ** External interface *)")
print ()
print ("(** We provide our main tactics:")
print ()
print ("    - [pcofix{n} ident using lemma with ident']")
print ()
print ()
print ("    where [ident] is the identifier used to name the generated coinduction hypothesis,")
print ("    [lemma] is an expression denoting which accumulation lemma is to be used, and")
print ("    [ident'] is the identifier used to name the accumulation variable.")
print ("*)")
print ()

for n in range(relsize+1):
    print ('Tactic Notation "pcofix'+str(n)+'" ident(CIH) "using" constr(lem) "with" ident(r) :=')
    print ('paco_pre'+str(n)+'; eapply lem; [..|paco_post'+str(n)+' CIH with r].')
    print ()

print ('(** [pcofix] automatically figures out the appropriate index [n] from')
print ('    the type of the accumulation lemma [lem] and applies [pcofix{n}].')
print ('*)')
print ()

print ('Tactic Notation "pcofix" ident(CIH) "using" constr(lem) "with" ident(nr) :=')
print ('  let N := fresh "_paco_N_" in let TMP := fresh "_paco_TMP_" in')
print ('  evar (N : nat);')
print ('  let P := type of lem in')
print ('  assert (TMP: False -> P) by')
print ('    (intro TMP; repeat intro; match goal with [H : _ |- _] => revert H end;')
print ('     match goal with')
for n in reversed(range(relsize+1)):
    print ('     | [|- _'+n*' _'+' -> _] => revert N; instantiate (1 := '+str(n)+')')
print ('     end; destruct TMP);')
print ('  clear TMP;')
print ('  revert N;')
print ('  match goal with')
for n in range(relsize+1):
    print ('  | [|- let _ := '+str(n)+' in _] => intros _; pcofix'+str(n)+' CIH using lem with nr')
print ('  end.')
print ()

print ('Tactic Notation "pcofix" ident(CIH) "using" constr(lem) :=')
print ('  pcofix CIH using lem with r.')
print ()

print ("""
(** ** Type Class for acc, mult, fold and unfold
*)

Class paco_class (A : Prop) :=
{ pacoacctyp: Type
; pacoacc : pacoacctyp
; pacomulttyp: Type
; pacomult : pacomulttyp
; pacofoldtyp: Type
; pacofold : pacofoldtyp
; pacounfoldtyp: Type
; pacounfold : pacounfoldtyp
}.

Create HintDb paco.
""")
