import pytest
from unittest import mock
import builtins
from uvsim import Machine
from Input import Input

def test_add():
    memory = [2000, 3001]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 5001

def test_add2():
    memory = [2000, 3000]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 4000

def test_subtract():
    memory = [2000, 3001, 3100]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 3001

def test_subtract2():
    memory = [2000, 3000, 3100]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 2000

def test_divide():
    memory = [2000, 3001, 3200]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 2

def test_divide2():
    memory = [2000, 3000, 3000, 3200]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 3

def test_multiply():
    memory = [2000, 3001, 3300]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 10002000

def test_multiply2():
    memory = [2000, 3000, 3301]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 12000000

def test_load():
    memory = [2000, 3001, 3300, 2002]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 3300

def test_load2():
    memory = [2000, 3301, 3202, 2002]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine.debug_get_accumulator() == 3202

def test_store():
    memory = [2000, 3001, 3300, 2000, 2106]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine._memory[6] == 2000

def test_store2():
    memory = [2000, 3001, 3300, 2002, 2106]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    assert machine._memory[6] == 3300

def test_read():
    # Test signed number
    memory = [1002]
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
    memory = [1002]
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
    memory = [1101, 4300]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    out, err = capfd.readouterr()
    assert out[-6:-1] == '+4300'
    # Test empty memory
    memory = [1102, 4300]
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()
    out, err = capfd.readouterr()
    assert out[-6:-1] == '+0000'
    

def test_branch():
    # Test branch ahead
    memory = [4002, 0000, 4300]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 2
    # Test branch behind
    memory = [4002, 4300, 4001]
    machine = Machine(memory)
    machine.tick()
    machine.tick()
    assert machine.debug_get_program_counter() == 1

def test_branch_neg():
    # Test non negative
    memory = [4102, 0000, 4300]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 1
    # Test negative
    memory = [4102, 0000, 4300]
    machine = Machine(memory)
    machine.debug_set_accumulator(-1)
    machine.tick()
    assert machine.debug_get_program_counter() == 2

def test_branch_zero():
    # Test non zero
    memory = [4202, 0000, 4300]
    machine = Machine(memory)
    machine.debug_set_accumulator(1)
    machine.tick()
    assert machine.debug_get_program_counter() == 1
    # Test zero
    memory = [4202, 0000, 4300]
    machine = Machine(memory)
    machine.tick()
    assert machine.debug_get_program_counter() == 2

def test_halt():
    memory = [4300]
    machine = Machine(memory)
    count = 0
    while machine.is_running():
        machine.tick()
        count += 1
    assert count == 1