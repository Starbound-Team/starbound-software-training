#include <stdio.h>

int main(){
    int a[2] = {1,2};
    if(!a[0] && a[999]){
        printf("a[0] is 0\n");
    }
    else printf("a[0] is non-0\n");

    if(a[0] > 0 || a[999]) printf("a[0] is actually positive\n");
}
