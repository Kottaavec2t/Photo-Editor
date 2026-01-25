"""Test suite for the new Command Pattern Undo/Redo System."""
import sys
import os
import tempfile
# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
from models.image_state import ImageStateManager
from models.command import (
    BrightnessCommand,
    RotationCommand,
    GrayscaleCommand,
    CommandGroup,
)

# Create a temporary directory for test images
TEMP_DIR = tempfile.gettempdir()


def test_individual_commands():
    """Test that individual commands work and are independently undoable."""
    print("Testing individual commands...")
    
    # Create a simple test image
    test_image = Image.new('RGB', (100, 100), color='red')
    
    # Save it temporarily
    test_path = os.path.join(TEMP_DIR, 'test_image.jpg')
    test_image.save(test_path)
    
    # Initialize state manager
    image_state = ImageStateManager()
    image_state.load_image(test_path)
    
    # Apply two separate commands
    cmd1 = BrightnessCommand(1.5)
    image_state.execute_command(cmd1)
    assert image_state.can_undo(), "Should be able to undo after first command"
    assert not image_state.can_redo(), "Should not be able to redo initially"
    
    cmd2 = RotationCommand(45)
    image_state.execute_command(cmd2)
    assert image_state.can_undo(), "Should be able to undo after second command"
    
    # Verify history
    history = image_state.get_history()
    assert len(history) == 2, f"Expected 2 commands in history, got {len(history)}"
    print(f"  History: {history}")
    
    # Undo second command
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 1, "Should have 1 command after undo"
    assert image_state.can_redo(), "Should be able to redo after undo"
    print("  ✓ Successfully undid individual command")
    
    # Undo first command
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 0, "Should have 0 commands after second undo"
    assert not image_state.can_undo(), "Should not be able to undo at start"
    print("  ✓ Successfully undid both commands individually")
    
    # Redo
    image_state.redo()
    history = image_state.get_history()
    assert len(history) == 1, "Should have 1 command after redo"
    print("  ✓ Successfully redid command")
    
    print("✓ Individual commands test PASSED\n")


def test_grouped_transactions():
    """Test that grouped commands are undone/redone as a unit."""
    print("Testing grouped transactions...")
    
    # Create a simple test image
    test_image = Image.new('RGB', (100, 100), color='blue')
    test_path = os.path.join(TEMP_DIR, 'test_image2.jpg')
    test_image.save(test_path)
    
    image_state = ImageStateManager()
    image_state.load_image(test_path)
    
    # Start a transaction
    image_state.begin_transaction("Adjust photo")
    
    cmd1 = BrightnessCommand(1.5)
    image_state.execute_command(cmd1)
    
    cmd2 = RotationCommand(30)
    image_state.execute_command(cmd2)
    
    # End transaction
    image_state.end_transaction()
    
    history = image_state.get_history()
    assert len(history) == 1, f"Expected 1 transaction in history, got {len(history)}"
    print(f"  History: {history}")
    assert "Adjust photo" in history[0], "Transaction should have the correct description"
    
    # Single undo should remove both commands
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 0, "Should have 0 commands after single undo of transaction"
    print("  ✓ Both commands undone with single undo (grouped)")
    
    # Single redo should restore both
    image_state.redo()
    history = image_state.get_history()
    assert len(history) == 1, "Should have 1 transaction after redo"
    print("  ✓ Both commands redone with single redo (grouped)")
    
    print("✓ Grouped transactions test PASSED\n")


def test_mixed_operations():
    """Test mixing grouped and individual commands."""
    print("Testing mixed operations...")
    
    test_image = Image.new('RGB', (100, 100), color='green')
    test_path = os.path.join(TEMP_DIR, 'test_image3.jpg')
    test_image.save(test_path)
    
    image_state = ImageStateManager()
    image_state.load_image(test_path)
    
    # Add an individual command
    cmd1 = BrightnessCommand(1.2)
    image_state.execute_command(cmd1)
    
    # Add a transaction
    image_state.begin_transaction("Color adjustments")
    cmd2 = RotationCommand(15)
    image_state.execute_command(cmd2)
    cmd3 = GrayscaleCommand()
    image_state.execute_command(cmd3)
    image_state.end_transaction()
    
    # Add another individual command
    cmd4 = BrightnessCommand(0.8)
    image_state.execute_command(cmd4)
    
    history = image_state.get_history()
    assert len(history) == 3, f"Expected 3 items in history, got {len(history)}"
    print(f"  History: {history}")
    
    # Undo should remove brightness command
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 2, "Should have 2 items after first undo"
    
    # Next undo should remove entire transaction
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 1, "Should have 1 item after second undo"
    
    # Next undo should remove first brightness
    image_state.undo()
    history = image_state.get_history()
    assert len(history) == 0, "Should have 0 items after third undo"
    
    print("  ✓ Mixed operations work correctly")
    print("✓ Mixed operations test PASSED\n")


def test_descriptions():
    """Test that command descriptions work."""
    print("Testing command descriptions...")
    
    test_image = Image.new('RGB', (100, 100), color='yellow')
    test_path = os.path.join(TEMP_DIR, 'test_image4.jpg')
    test_image.save(test_path)
    
    image_state = ImageStateManager()
    image_state.load_image(test_path)
    
    # Add commands with various values
    image_state.execute_command(BrightnessCommand(1.75))
    image_state.execute_command(RotationCommand(45.5))
    image_state.execute_command(GrayscaleCommand())
    
    history = image_state.get_history()
    print(f"  History descriptions: {history}")
    
    assert "1.75" in history[0], "Brightness value should be in description"
    assert "45.5" in history[1], "Rotation angle should be in description"
    assert "Grayscale" in history[2], "Grayscale should be in description"
    
    # Check undo/redo descriptions
    undo_desc = image_state.get_undo_description()
    print(f"  Undo description: {undo_desc}")
    assert undo_desc == "Grayscale", "Undo description should match top of stack"
    
    image_state.undo()
    redo_desc = image_state.get_redo_description()
    print(f"  Redo description: {redo_desc}")
    assert redo_desc == "Grayscale", "Redo description should match what we just undid"
    
    print("✓ Descriptions test PASSED\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Command Pattern Undo/Redo System Tests")
    print("=" * 60 + "\n")
    
    try:
        test_individual_commands()
        test_grouped_transactions()
        test_mixed_operations()
        test_descriptions()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
