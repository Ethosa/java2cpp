# -*- coding: utf-8 -*-
# author: Ethosa

from java2cpp import Java2Cpp

j = Java2Cpp()

text = """
// Hello world program
class Main {
    public static void main(String[] args){
        System.out.println("Hello world");
        System.out.print("ban");
        var a = 1;

        for (int i = 0; i < 100; ++i){
            System.out.println(test());
        }
    }
    public static int test(){
        var r = new Random();
        int b = 5 + r.nextInt(64 - 5 + 1);
        return b;
    }
    public String test(String a){
        long i = 100L;
        long j = 100_000L;
        String timed = "timed";
        return timed + a;
    }
}"""

print(j.translate(text))
