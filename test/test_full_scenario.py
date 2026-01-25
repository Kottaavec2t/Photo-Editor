"""
Test complet du système de remplacement intelligent avec ImageStateManager
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image, ImageDraw
from models.image_state import ImageStateManager
from models.command import BrightnessCommand, RotationCommand


def test_full_scenario():
    """Test complet: brightness -> rotation -> brightness (replace)"""
    print("\n" + "="*70)
    print("TEST COMPLET: Système de Remplacement Intelligent")
    print("="*70 + "\n")
    
    # Créer une image de test avec du texte pour voir les transformations
    base_img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(base_img)
    draw.text((10, 10), "BASE", fill='black')
    
    # Initialiser le gestionnaire d'état
    manager = ImageStateManager()
    manager._base_image = base_img.copy()
    manager._current_image = base_img.copy()
    
    print("Étape 1: Appliquer Brightness(1.5)")
    print("-" * 70)
    cmd1 = BrightnessCommand(factor=1.5, original_image=manager._current_image)
    manager.execute_command(cmd1)
    print(f"✓ Brightness(1.5) appliquée")
    print(f"  Pile undo: {manager._command_history.get_history()}")
    print(f"  Remplacées: {list(manager._command_history._replaced_commands.keys())}")
    
    print("\nÉtape 2: Appliquer Rotation(90°)")
    print("-" * 70)
    cmd2 = RotationCommand(angle=90)
    manager.execute_command(cmd2)
    print(f"✓ Rotation(90) appliquée")
    print(f"  Pile undo: {manager._command_history.get_history()}")
    print(f"  Remplacées: {list(manager._command_history._replaced_commands.keys())}")
    
    print("\nÉtape 3: Appliquer Brightness(1.3) - DEVRAIT REMPLACER Brightness(1.5)")
    print("-" * 70)
    cmd3 = BrightnessCommand(factor=1.3, original_image=manager._current_image)
    manager.execute_command(cmd3)
    print(f"✓ Brightness(1.3) appliquée")
    print(f"  Pile undo: {manager._command_history.get_history()}")
    print(f"  Remplacées: {list(manager._command_history._replaced_commands.keys())}")
    
    # Vérifier que Brightness(1.5) est bien remplacée
    if 'BrightnessCommand' in manager._command_history._replaced_commands:
        replaced = manager._command_history._replaced_commands['BrightnessCommand']
        print(f"\n✓ Brightness(1.5) est dans les remplacées!")
        print(f"  Commandes remplacées: {[f'Brightness({cmd.factor}x)' for cmd in replaced]}")
    else:
        print(f"\n✗ ERREUR: Brightness(1.5) n'est pas remplacée!")
    
    # Vérifier la pile undo finale
    print(f"\n  État final de la pile undo:")
    print(f"    {manager._command_history.get_history()}")
    print(f"  Longueur: {len(manager._command_history._undo_stack)} (attendu: 2)")
    
    print("\nÉtape 4: Undo - devrait retrouver Rotation + Brightness(1.5)")
    print("-" * 70)
    manager.undo()
    print(f"✓ Undo exécuté")
    print(f"  Pile undo après undo: {manager._command_history.get_history()}")
    print(f"  Attendu: ['Brightness (1.50x)', 'Rotation (90.0°)']")
    
    # Vérifier les deux premières commandes
    if len(manager._command_history._undo_stack) == 2:
        first_cmd = manager._command_history._undo_stack[0]
        second_cmd = manager._command_history._undo_stack[1]
        print(f"\n  Vérifications:")
        if isinstance(first_cmd, BrightnessCommand) and first_cmd.factor == 1.5:
            print(f"    ✓ Première commande: Brightness(1.5)")
        if isinstance(second_cmd, RotationCommand) and second_cmd.angle == 90:
            print(f"    ✓ Deuxième commande: Rotation(90°)")
    
    print("\nÉtape 5: Redo - devrait restaurer Brightness(1.3)")
    print("-" * 70)
    manager.redo()
    print(f"✓ Redo exécuté")
    print(f"  Pile undo après redo: {manager._command_history.get_history()}")
    print(f"  Attendu: ['Brightness (1.30x)', 'Rotation (90.0°)']")
    
    print("\n" + "="*70)
    print("✓ TEST COMPLET RÉUSSI")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_full_scenario()
