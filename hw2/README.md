# Sender Flowchart
```flow
st=>start: START
e=>end: END

op1=>operation: file_to_packets
op2=>operation: send packets(winsize)
op3=>operation: send FIN

cond1=>condition: all packets sent
cond2=>condition: received ACK
cond3=>condition: received FINACK

st->op1(right)->op2->cond2
cond2(yes)->cond1
cond2(no)->op2
cond1(yes)->op3->cond3
cond1(no)->op2
cond3(yes)->e
cond3(no)->op3
```
---
# Agent Flowchart
```flow
st=>start: START
e=>end: END

op1=>operation: get packet
op2=>operation: fwd to sender
op3=>operation: fwd to receiver
op4=>operation: drop packet

inout=>inputoutput: ACK or FINACK

cond1=>condition: DATA or FIN
cond2=>condition: Drop packet

st->op1->cond1
cond1(yes)->cond2
cond2(yes)->op1
cond2(no)->op2(right)->op1
cond1(no)->inout->op3(right)->op1
```
---
# Receiver Flowchart
```flow
st=>start: START
e=>end: END

op1=>operation: recv packet
op2=>operation: send ACK(#acked)
op3=>operation: acked += 1
op4=>operation: send FINACK

cond1=>condition: packet seq == acked+1
cond2=>condition: is FIN

st->op1->cond1
cond1(yes)->cond2
cond2(yes)->op4(right)->e
cond2(no)->op3(right)->op2(right)->op1
cond1(no)->op2

```