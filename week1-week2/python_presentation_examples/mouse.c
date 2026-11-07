#include <stdio.h>

typedef struct Mouse Mouse;

// The type: one shared table per kind of thing, holding its functions.
// In Python this is the class, e.g. type(a) -> <class 'list'>
typedef struct {
    const char *name;
    void (*move)(Mouse *self, int dx, int dy);
    void (*click)(Mouse *self);
} MouseType;

// The object: its own data, plus a pointer to its type
struct Mouse {
    const MouseType *type;
    int x, y;
    int clicks;
};

void mouse_move(Mouse *self, int dx, int dy) {
    self->x += dx;
    self->y += dy;
}

void mouse_click(Mouse *self) {
    self->clicks++;
    printf("click at (%d, %d)\n", self->x, self->y);
}

const MouseType MOUSE = { "Mouse", mouse_move, mouse_click };

int main(void) {
    Mouse a = { &MOUSE, 0, 0, 0 };
    Mouse b = { &MOUSE, 0, 0, 0 };

    // Python: a.move(5, 3)
    // look up move in a's type, call it with a as the first argument
    a.type->move(&a, 5, 3);
    a.type->click(&a);

    // b is a separate mouse with its own data
    b.type->click(&b);

    // Python: c = a  (another name for the same mouse)
    Mouse *c = &a;
    c->type->click(c);

    printf("a: %d clicks, b: %d clicks\n", a.clicks, b.clicks);
    printf("type of a: %s\n", a.type->name);
    return 0;
}
