




var maxsize = 100, m = 0, n = 0; //m行数 n列数
var a = new Array(maxsize + 1).fill((new Array(maxsize + 1)).fill(0.0));
var eps = 0.0000000001;
var i = 0, j = 0;

a = [[1, 3, 5, 5], [6, 4, 3, 8], [7, 6, 8, 0], [1, 9, 3, 4], [6, 7 , 0, 8]];
m = 5;
n = 4;

for (var r = 0, c = 0; c < n && r<m; c++)   //遍历每一列
{
    var t = r;
    for (var i = r; i < m; i++)                       //找到这一列中元素最大的一行
        if (Math.abs(a[i][c]) > Math.abs(a[t][c]))
            t = i;
    if (Math.abs(a[t][c]) < eps) continue;    //如果元素最大，还是0，那就跳过，去处理下一列
    for (var i = 0; i < n; i++) {
        // swap(a[t][i], a[r][i]);
        var temp = a[t][i];
        a[t][i] = a[r][i];
        a[r][i] = temp;
    }
    //把选中的这一行放到“最上面”去
    var d = a[r][c];
    for (var i = 0; i < n; i++) a[r][i] /= d;    //把这一行的第c列化成1
    for (var i = r + 1; i < m; i++)             //把其他行的第c列消成0
        if (Math.abs(a[i][c]) > eps) {
            var p = a[i][c];
            for (var j = 0; j < n; j++)
                a[i][j] -= p * a[r][j];
        }
    r++;
}
/*
if(r<n)     //如果最后不是严格完全的阶梯型
{
    for(var i=r;i<n;i++)
        if(Math.abs(a[i][n])>eps)      //0==非零的情况，无解
            return 2;
    return 1;        //0==0的情况，有无穷多解
}
for(var i=n-1;i>=0;i--)                //从下往上的把解给求出来
    for(var j=i+1;j<n;j++)
        a[i][n]-=a[j][n]*a[i][j];
return 0;
*/
console.log(a)


for(var r=m-1; r>=0; --r) {
    //找第一个不为0的
    var zyl = -1;
    for(var c=0; c<n; ++c) {
        if(Math.abs(a[r][c])>eps) {
            zyl = c;
            break;
        }
    }
    if(zyl == -1) {//这一行都是0
        continue;
    }
    if(zyl == n-1) {
        break;
    }
    //除了这一行是1，主元列必须是0
    for(var i=0; i<r; ++i) { //这一行 -= a[i][zyl] * r行
        var p = a[i][zyl];
        for(var j=0; j<n; ++j) {
            a[i][j] -= p * a[r][j];
        }
    }
}

console.log(a)
