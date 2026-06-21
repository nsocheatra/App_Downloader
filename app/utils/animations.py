import math

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*(max(0, min(255, int(c))) for c in rgb))

def interpolate_color(color_start, color_end, progress):
    try:
        rgb_start = hex_to_rgb(color_start)
        rgb_end = hex_to_rgb(color_end)
        rgb_curr = tuple(
            start + (end - start) * progress
            for start, end in zip(rgb_start, rgb_end)
        )
        return rgb_to_hex(rgb_curr)
    except Exception:
        return color_end

class WidgetAnimator:
    """Manages smooth property transitions for Tkinter/CustomTkinter widgets."""
    def __init__(self, widget):
        self.widget = widget
        self._active_animations = {}

    def animate_color(self, config_key, start_color, end_color, duration_ms=200, steps=10, callback=None):
        """Animates a color property (e.g., 'fg_color', 'border_color')."""
        self.cancel(config_key)
        
        step_time = max(5, duration_ms // steps)
        
        def run_step(step=0):
            if not self.widget.winfo_exists():
                return
            
            progress = step / steps
            # Smooth ease-in-out curve
            ease_progress = (1 - math.cos(progress * math.pi)) / 2
            current_color = interpolate_color(start_color, end_color, ease_progress)
            try:
                self.widget.configure(**{config_key: current_color})
            except Exception:
                pass
            
            if callback:
                callback(current_color)

            if step < steps:
                anim_id = self.widget.after(step_time, lambda: run_step(step + 1))
                self._active_animations[config_key] = anim_id
            else:
                self._active_animations.pop(config_key, None)

        run_step(0)

    def animate_float(self, anim_name, start_val, end_val, update_func, duration_ms=300, steps=15, callback=None):
        """Animates a floating point value (e.g. progress bar fraction)."""
        self.cancel(anim_name)
        
        step_time = max(5, duration_ms // steps)
        
        def run_step(step=0):
            if not self.widget.winfo_exists():
                return
            
            progress = step / steps
            # Smooth ease-out cubic
            ease_progress = 1 - (1 - progress) ** 3
            current_val = start_val + (end_val - start_val) * ease_progress
            
            try:
                update_func(current_val)
            except Exception:
                pass

            if step < steps:
                anim_id = self.widget.after(step_time, lambda: run_step(step + 1))
                self._active_animations[anim_name] = anim_id
            else:
                if callback:
                    callback()
                self._active_animations.pop(anim_name, None)

        run_step(0)

    def cancel(self, name):
        if name in self._active_animations:
            try:
                self.widget.after_cancel(self._active_animations[name])
            except Exception:
                pass
            self._active_animations.pop(name, None)

    def cancel_all(self):
        for name in list(self._active_animations.keys()):
            self.cancel(name)


class PulseAnimator:
    """Creates a continuous breathing/pulsing effect for a widget's color."""
    def __init__(self, widget, config_key, color1, color2, duration_ms=1800, steps=30):
        self.widget = widget
        self.config_key = config_key
        self.color1 = color1
        self.color2 = color2
        self.duration_ms = duration_ms
        self.steps = steps
        self.running = False
        self._after_id = None

    def start(self):
        if self.running:
            return
        self.running = True
        self._pulse_cycle(0, 1)

    def stop(self):
        self.running = False
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _pulse_cycle(self, step, direction):
        if not self.running or not self.widget.winfo_exists():
            return
        
        progress = step / self.steps
        ease_progress = (math.sin((progress - 0.5) * math.pi) + 1) / 2
        
        curr_color = interpolate_color(self.color1, self.color2, ease_progress)
        try:
            self.widget.configure(**{self.config_key: curr_color})
        except Exception:
            pass

        next_step = step + direction
        next_direction = direction
        if next_step >= self.steps:
            next_direction = -1
        elif next_step <= 0:
            next_direction = 1

        step_time = max(5, self.duration_ms // self.steps)
        self._after_id = self.widget.after(step_time, lambda: self._pulse_cycle(next_step, next_direction))
