import pytest
from unittest import mock
import builtins
from uvsim import Machine
from Input import Input

def test_add():
    memory = [20000, 30001]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 50001

def test_add2():
    memory = [20000, 30000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 40000

def test_subtract():
    memory = [20000, 30001, 31000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 30001

def test_subtract2():
    memory = [20000, 30000, 31000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 20000

def test_divide():
    memory = [20000, 30001, 32000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 2

def test_divide2():
    memory = [20000, 30000, 30000, 32000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 3

def test_multiply():
    memory = [20000, 30001, 33000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 1000020000

def test_multiply2():
    memory = [20000, 30000, 33001]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 1200000000

def test_load():
    memory = [20000, 30001, 33000, 20002]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 33000

def test_load2():
    memory = [20000, 33001, 32002, 20002]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 32002

def test_store():
    memory = [20000, 30001, 33000, 20000, 21006]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine._memory[6] == 20000

def test_store2():
    memory = [20000, 30001, 33000, 20002, 21006]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine._memory[6] == 33000

def test_read():
    # Test signed number
    memory = [10002]
    machine = Machine(memory)
    with mock.patch.object(builtins, 'input', lambda _: '-1234'):
        while machine.is_running():
            machine.tick()
            if machine.get_needs_input() > -1:
                input = Input()
                word = input.get_input()
                machine.set_memory_at_address(machine.get_needs_input(), int(word))
    assert machine._memory[2] == -1234
    
    # Test unsigned number
    memory = [10002]
    machine = Machine(memory)
    with mock.patch.object(builtins, 'input', lambda _: '1234'):
        while machine.is_running():
            machine.tick()
            if machine.get_needs_input() > -1:
                input = Input()
                word = input.get_input()
                machine.set_memory_at_address(machine.get_needs_input(), int(word))
    assert machine._memory[2] == 1234

def test_write(capfd):
    # Test occupied memory
    memory = [11001, 43000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    out, err = capfd.readouterr()
    assert machine.get_memory_at_address(1) == 43000
    # Test empty memory
    memory = [1102, 4300]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    out, err = capfd.readouterr()
    
    assert machine.get_memory_at_address(2) == 0
    

def test_branch():
    # Test branch ahead
    memory = [40002, 00000, 43000]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 2
    # Test branch behind
    memory = [40002, 43000, 40001]
    machine = Machine(memory)
    machine.tick()
    machine.tick()
    assert machine.debug_get_program_counter() == 1

def test_branch_neg():
    # Test non negative
    memory = [41002, 00000, 43000]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 1
    # Test negative
    memory = [41002, 00000, 43000]
    machine = Machine(memory)
    machine.debug_set_accumulator(-1)
    machine.tick()
    assert machine.debug_get_program_counter() == 2

def test_branch_zero():
    # Test non zero
    memory = [42002, 00000, 43000]
    machine = Machine(memory)
    machine.debug_set_accumulator(1)
    machine.tick()
    assert machine.debug_get_program_counter() == 1
    # Test zero
    memory = [42002, 00000, 43000]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 2

def test_halt():
    memory = [43000]
    machine = Machine(memory)
    count = 0
    while machine.is_running():
        machine.tick()
        count += 1
    assert count == 1