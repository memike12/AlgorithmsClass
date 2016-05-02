/* SI 335 Spring 2015
 * Project 2, RSA program
 * YOUR NAME HERE
 */

#include <unistd.h>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "posint.hpp"

using namespace std;

// Prints a message on proper usage and exits with the given code
void usage (const char* progname, int ret);

// Function prototype. You have to fill in the implementation below.
void powmod (PosInt& result, const PosInt& a, const PosInt& b, const PosInt& n);

// Determines if the provided number is prime
bool isPrime(PosInt n);

int main (int argc, char** argv) {
  // Detect if standard in is coming from a terminal
  bool interactive = isatty(fileno(stdin));

  // Seed the random number generator
  srand (time(NULL));

  // Pick the base to use in the PosInt class
  PosInt::setBase (10);

  // These parameters determine the blocking of characters
  PosInt byte(256);
  int blocklen = 10;
  PosInt topByte(1);
  for (int i=0; i<blocklen-1; ++i) topByte.mul(byte);

  if (argc < 2 || argv[1][0] != '-') usage(argv[0],1);
  if (argv[1][1] == 'k') {
    if (argc != 4) usage(argv[0],3);
    ofstream pubout(argv[2]);
    ofstream privout(argv[3]);
    if (! pubout || ! privout) {
      cerr << "Can't open public/private key files for writing" << endl;
      return 4;
    }
    ////////////////////////////////////////////////////////////////////
    //                 KEY GENERATION                                 //
    ////////////////////////////////////////////////////////////////////
    
    //Pick a number to start out with
    PosInt exp (80);
    PosInt randMax (2);
    randMax.pow(exp);

    //declare random numbers and n and totent(n)
    PosInt FirstRandomNumber(1);
    PosInt SecondRandomNumber(1);

    int primeTester;
    //Generate random numbers between 0 and rand max
    do {
      primeTester = 0;
      FirstRandomNumber.rand(randMax);
    
      //add randMax to the random number to ensure that both are at least randMax size
      FirstRandomNumber.add(randMax);

      //test each random number for primality 6 times
      for(int x = 0; x < 6; x++){
        if(FirstRandomNumber.MillerRabin()== true)
          primeTester++;
      }
    } while(primeTester < 6);
    do {
      primeTester = 0;
      SecondRandomNumber.rand(randMax);
    
      //add randMax to the random number to ensure that both are at least randMax size
      SecondRandomNumber.add(randMax);

      //test each random number for primality 6 times
      for(int x = 0; x < 6; x++){
        if(SecondRandomNumber.MillerRabin()== true)
           primeTester++;
      }
    } while(primeTester < 6);


    cout << "P = " << FirstRandomNumber << endl;
    cout << "Q = " << SecondRandomNumber << endl;

    //make n
    PosInt n (1);
    n.mul(FirstRandomNumber);
    n.mul(SecondRandomNumber);
    cout << "n = " << n << endl;
    
    //make totient(n)
    PosInt p(1);
    p.set(FirstRandomNumber);
    PosInt q(1);
    q.set(SecondRandomNumber);
    PosInt one(1);
    p.sub(one);
    q.sub(one);
    PosInt totient(1);
    totient.set(p);
    totient.mul(q);
    cout << "totient =" << totient << endl;

    //find e
    PosInt e (1);
    PosInt gcd(1);
    PosInt two(2);
    do{
       e.rand(totient);
       gcd.gcd(e, totient);
    }while ((!gcd.isOne())  ||  (e.compare(two)!=1));
    cout << "e =" << e << endl;
    cout << "gcd is " << gcd << endl;
    //find d
    PosInt d (1);
    PosInt t (1);
    PosInt s (1);
    PosInt g (1);
    
    g.xgcd(s,t,totient, e);

    d.set(t);
    d.add(totient);



    ////////////////////////////////////
    ////////////////////////////////////////
    /////Test POWMOD//////////
    PosInt result (1);
    PosInt a(21231237);
    a.mul(a);
    PosInt b(2013242123);
    b.mul(b);
    PosInt n1(1235453011);
    n1.mul(n1);
    powmod(result, a, b, n1);
    cout << a << "^" << b << " mod " << n1 <<  " =  " << result << endl;

    // Print out the keys to their respective files.
    pubout << e << endl << n << endl;
    privout << d << endl << n << endl;
    
    ///////////////// (end of key generation) //////////////////////////
    pubout.close();
    privout.close();
    if (interactive)
      cerr << "Public/private key pair written to " << argv[2]
           << " and " << argv[3] << endl;
  }
  else if (argv[1][1] == 'e') {
    if (argc != 3) usage(argv[0],3);
    ifstream pubin (argv[2]);
    if (! pubin) {
      cerr << "Can't open public key file for reading" << endl;
      return 4;
    }
    if (interactive)
      cerr << "Type your message, followed by EOF (Ctrl-D)" << endl;
    ////////////////////////////////////////////////////////////////////
    //                  ENCRYPTION WITH PUBLIC KEY                    //
    ////////////////////////////////////////////////////////////////////
    // Read public key from pubin file
    PosInt e, n;
    pubin >> e >> n;

    // Read characters from standard in and encrypt them
    int c;
    PosInt M (0); // Initialize M to zero
    PosInt curByte (topByte);

    bool keepGoing = true;
    while (keepGoing) {
      c = cin.get();
      //cout << "c is: " << c << endl;

      if (c < 0) keepGoing = false; // c < 0 means EOF or error.

      else {
        PosInt next (c); // next character, converted to a PosInt
        next.mul(curByte); // next *= curByte
        M.add(next);     // M = M + next
        curByte.div(byte);
      }

      if (curByte.isZero() || (!keepGoing && !M.isZero())) {
        // HERE'S WHERE YOU HAVE TO DO THE ENCRYPTION!
        PosInt result (1);
        cout << endl;
        cout <<  M << "^" << e << " mod " << n << endl;
        powmod(result, M, e, n);
        cout << result << endl;
        PosInt E(1);
        E.set(result); 
        cout << E << endl;

        // Now reset curByte and M and keep going
        curByte.set(topByte);
        M.set(0);
      }
    }
    ////////////////// (end of encryption) /////////////////////////////
    if (interactive)
      cerr << "Message successfully encrypted." << endl;
    pubin.close();
  }
  else if (argv[1][1] == 'd') {
    if (argc != 3) usage(argv[0],3);
    ifstream privin (argv[2]);
    if (! privin) {
      cerr << "Can't open private key file for reading" << endl;
      return 4;
    }
    if (interactive)
      cerr << "Enter encrypted numbers, one at a time, ending with EOF" << endl;
    ////////////////////////////////////////////////////////////////////
    //                 DECRYPTION WITH PRIVATE KEY                    //
    ////////////////////////////////////////////////////////////////////
    // Get private key from file
    PosInt d, n;
    privin >> d >> n;

    // Read numbers from standard in and decrypt them
    PosInt E;
    PosInt two56 (256);
    while (cin >> E) {
      // You have to decrypt E and print out the 10 characters it holds.
      // Note: use the "convert" function to turn a PosInt into
      // a regular "int" - and then into a char!.
      // Follow the procedure from encryption, only in reverse.
      PosInt M;
      PosInt divide;
      PosInt Letter;
      double dividend;
      int quotient;
      //int remainder;
      char letter;
      
      //char H = 'h';
      cout << endl;

      cout <<  E << "^" << d << " mod " << n << endl;

      powmod(M, E, d, n);

      cout << M << endl;
      for( int i = 9; i >= 0; i--){;
        //int mInt = M.convert();
        dividend = pow(256, i);
        divide.set(dividend);
        Letter.set(M);
        Letter.div(divide);
        quotient = Letter.convert();
        M.mod(divide);
        letter = quotient;
        //cout << quotient;
        cout << letter;
        //M.set(remainder);
      }
      cout << letter; // THIS IS JUST A DUMMY!
    }
    ////////////////// (end of decryption) /////////////////////////////
    if (interactive)
      cerr << "Message successfully decrypted." << endl;
    privin.close();
  }
  else if (argv[1][1] == 'h') usage(argv[0], 0);
  else usage(argv[0],2);
  return 0;
}

////////////////////////////////////////////////////////////
//              MODULAR EXPONENTIATION                    //
////////////////////////////////////////////////////////////

// Computes a^b mod n, and stores the answer in "result".
void powmod (PosInt& result, const PosInt& a, const PosInt& b, const PosInt& n) {
  //cout << "Got result: " << result << " and a: " << a << " and b: " << b << " and n: " << n << endl;
  PosInt three(3);
  if(b.compare(three) == 1){// ||  b.compare(three) == 0 ){
    PosInt two(2);
    PosInt remainder (1);
    PosInt quotient (1);
    PosInt A (a);
    //Find remainder
    remainder.set(b);
    remainder.mod(two);

    //Find Quotient
    quotient.set(b);
    quotient.div(two);

    //Recurse
    powmod(result, a, quotient, n);
    
    //Figure out answer
    if(remainder.isOne()){
      result.mul(result);
      result.mod(n);
      result.mod(n);
      A.mod(n);
      result.mul(A);
      result.mod(n);
      //cout << "found: " << result << endl;
      return;
    }
    else{
      result.mul(result);
      result.mod(n);
      //cout << "found: " << result << endl;
    }
  }
  else{
    if( b.compare(three) == 0){
      result.set(a);
      PosInt A (a);
      result.mul(result);
      result.mod(n);
      A.mod(n);
      result.mul(A);
      result.mod(n);
      //cout << "found: " << result << endl;
    }

    else {
      //cout << "result first: " << result << endl; 
    result.set(a);
    //cout << "result set to a: "<< result << endl;
    result.mod(n);
    //cout << "a mod n = " << result << endl;
    //result.mul(result);
    //cout << "multiply it by itself: " << result << endl;
    result.mod(n);
    //cout << "found: " << result << endl;
    return;
    }
  }
}


////////////////////////////////////////////////////////////
//              KARATSUBA MULTIPLICATION                  //
////////////////////////////////////////////////////////////

// Sets "this" PosInt object to "this" times x.
void PosInt::fasterMul (const PosInt& x) {
  // This is a suggestion of how to do this one:

  // First figure out the larger of the two input sizes
  int n = digits.size();
  if (n < x.digits.size()) n = x.digits.size();
  
  // Now copy the inputs into vectors of that size, with zero-padding
  vector<int> mycopy(digits);
  vector<int> xcopy(x.digits);
  mycopy.resize(n, 0);
  xcopy.resize(n, 0);

  // Set "this" digit vector to a zeroed-vector of size 2n
  digits.assign (2*n, 0);

  // Now call the array version to do the actual multiplication
  fastMulArray (&digits[0], &mycopy[0], &xcopy[0], n);

  // We have to call normalize in case there are leading zeros
  normalize();
}

// This does the real work of Karatsuba's algorithm
// (or whatever multiplication algorithm you might write).
// The input is two arrays of digits, x and y, which both have length len.
// The output is stored in the array dest, which is already allocated
// to the proper length.
void PosInt::fastMulArray (int* dest, const int* x, const int* y, int len) {
  int* A = new int[2*len +1];
  if (len <= 3) {
    // base case
    // YOU FILL THIS IN
   *dest = (*x)*(*y);
   return;
  }
  else {
    // recursive case
    // YOU FILL THIS IN TOO.
    // Hint: you will have to allocate some memory for U, V, P0, P1, and P2
    // Another hint: use the addArray and subArray helper methods from the
    // PosInt class!
    double lenover2 = len/2;
    int floora = floor(lenover2);
    int ceila= ceil(lenover2);
    int* X0 = new int[floora];
    int* X1 = new int[ceila];
    int* Y0 = new int[floora];
    int* Y1 = new int[ceila];
    int X = *x;
    int Y = *y;
    for(int i = 0; i < len; i++){
      if(i < floor(len/2)){
        X0[i] = X %10;
        X = X /10;
        Y0[i] =Y %10;
        Y = Y/10;
      }
      else{
        X1[i - floora] =  X %10;
        X =X /10;
        Y1[i - floora] =Y %10;
        Y = Y/10;
      }
      
    }
    int* U = X0;
    addArray (U,  X1, len);
    int* V = Y0;
    addArray (V,  Y1, len);
    int size = 2*lenover2;
    int* P0 = new int[size];
    int* P1 = new int[size];
    int* P2 = new int[size];
    
    fastMulArray(P0, X0, Y0, floor(len/2));
    fastMulArray(P1, X1, Y1, ceil(len/2));
    fastMulArray(P2, U, V, floor(len/2));
    int total = lenover2*2;

    //A[0 : 2*m] = P0;
    for (int it = 0; it < total; it++ ){
      A[it] = P0[it];
    }
    
    // A[2*m : 2*n] = P1;
    for (int it = total; it < total+2*len; it++ ){
      A[it] = P1[it-total];
    }
    total += 2*len;

    //A[m : 2*n+1] = add(A[m : 2*n], P2, B);
    for (int it = lenover2; it < 2*len+1; it++ ){
      A[it] = P1[it-total];
    }


    //A[m : 2*n+1] = sub(A[m : 2*n+1], P0, B);
    //A[m : 2*n+1] = sub(A[m : 2*n+1], P1, B);
      
    
  }
}


// Prints a message on proper usage and exits with the given code
void usage (const char* progname, int ret) {
  cout
    << "Generate a public-private key pair:" << endl
    << "\t" << progname << " -k PUBLIC_KEY_FILE PRIVATE_KEY_FILE" << endl
    << "Encrypt a message with public key:" << endl
    << "\t" << progname << " -e PUBLIC_KEY_FILE" << endl
    << "Decrypt a message with private key:" << endl
    << "\t" << progname << " -d PRIVATE_KEY_FILE" << endl
    << "Note: PUBLIC_KEY_FILE and PRIVATE_KEY_FILE are any filenames you choose."
    << endl
    << "      Encryption and decryption read and write to/from standard in/out."
    << endl
    << "      You have to end the input with EOF (Ctrl-D if on command line)."
    << endl
    << "      You can use normal bash redirection with < and > to read or" << endl
    << "      write the encryption results to a file instead of standard in/out."
    << endl;
  exit(ret);
}

